import asyncio
import aioschedule
from aiogram import Bot
from aiogram.types import User, Message, ParseMode

from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.StorageManager.StorageManager as storage
import Core.TrelloService as trello
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class OrderCreationEntities:

    # userLoadingMessage: Message = None
    user: User = None
    channelPost: Message = None
    treloCard: dict
    userRequest: dict

    def __init__(
        self,
        # userLoadingMessage: Message,
        user: User,
        channelPost: Message,
        treloCard: dict,
        userRequest:dict
    ):
        # self.userLoadingMessage = userLoadingMessage
        self.user = user
        self.channelPost = channelPost
        self.treloCard = treloCard
        self.userRequest = userRequest

orderCreationEntities = {}
telegramServiceMessagesToReply = {}
sleepTime = 6

class CrossDialogMessageSender:

    bot: Bot
    channel: str

    def __init__(self, bot: Bot, channel: str):
        self.bot = bot
        self.channel = channel

    def configureBackgroundTasks(self):
        aioschedule.every(sleepTime).seconds.do(self.orderCreationRegularTask)

    async def threadedTasks(self):
        log.info("Tasks thread start")
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(sleepTime)

    async def setWaitingForOrder(self, userTg: User, msgText: str):
        message = await self.bot.send_message(
            chat_id = self.channel,
            text=msgText
        )

        userRequest = storage.getUserRequest(userTg)
        bikeName = "None"
        if RequestCodingKeys.bikeMotoCategory.get in userRequest:
            bikeName = userRequest[RequestCodingKeys.bikeMotoCategory.get]["value"]
        if RequestCodingKeys.bikeScooterCategory.get in userRequest:
            bikeName = userRequest[RequestCodingKeys.bikeScooterCategory.get]["value"]

        # TODO: implement test env to evoid terllo card creation while testing
        trelloCardTitle = f"@{userTg.username}: {bikeName}"
        # response = trello.createCard(
        #     title = trelloCardTitle,
        #     description = f"https://t.me/{userTg.username}\n{msgText}"
        # )
        orderCreationEntities[message.text] = OrderCreationEntities(
            user = userTg,
            channelPost = message,
            treloCard = {
                # "id": response["id"],
                "id": 228,
                "title": trelloCardTitle
            },
            userRequest = userRequest
        )

    async def makeAnOrderWithChannelChatMessageCtx(self, ctx: Message):
        telegramServiceMessagesToReply[ctx.text] = ctx

    async def orderCreationRegularTask(self):
        log.info(f"len orderCreationEntities: {len(orderCreationEntities)}; len telegramServiceMessagesToReply: {len(telegramServiceMessagesToReply)}")

        if len(telegramServiceMessagesToReply) == 0:
            return

        orders = [messageText for messageText in telegramServiceMessagesToReply if messageText in orderCreationEntities]
        for messageText in orders:

            orderCreationEntity: OrderCreationEntities = orderCreationEntities[messageText]
            telegramServiceMessage: Message = telegramServiceMessagesToReply[messageText]

            channelChatId = telegramServiceMessage.chat.id
            channelChatMessageId = telegramServiceMessage.message_id
            orderId = channelChatMessageId

            text = messageText
            userTg = orderCreationEntity.user
            channelMessage: Message = orderCreationEntity.channelPost
            await channelMessage.edit_text(
                text=f"<b>id{orderId}</b>\n{text}",
                parse_mode=ParseMode.HTML
            )

            orderData = {
                "id": orderId,
                "orderVersion": "1.1.0",
                "channelMessageId": channelMessage.message_id,
                "channelChatId": channelChatId,
                "channelChatMessageId": channelChatMessageId,
                "status": "Создан",
                "trelloCard": orderCreationEntity.treloCard,
                "text": text
            }

            userInfo = storage.getUserInfo(userTg)
            if "orders" in userInfo:
                userInfo["orders"].append(orderData)
            else:
                userInfo["orders"] = [orderData]
            storage.updateUserData(userTg, userInfo)

            orderData["userInfo"] = userInfo["info"]
            storage.updateOrderData(
                orderId=orderId,
                data=orderData
            )

            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"Пользователь завершил создание заказа",
                reply_to_message_id=channelChatMessageId
            )

            text = textConstant.orderCreationUserText.getAndReplaceOrderMaskWith(f'{orderId}')
            await self.bot.send_message(
                chat_id = userTg.id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )

            trello.updateCardTitle(
                id=orderCreationEntity.treloCard["id"],
                title=f"id{orderId} {orderCreationEntity.treloCard['title']}"
            )

            del orderCreationEntities[messageText]
            del telegramServiceMessagesToReply[messageText]

    async def forwardMessageFromManagerToUser(self, ctx, order):

        channelChatId = order["userInfo"]["id"]
        orderId = order["id"]
        text = textConstant.orderDetailsMessageTitle.getAndReplaceOrderMaskWith(f'{orderId}')
        if ctx.text != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"{text}\n{ctx.text}",
                parse_mode=ParseMode.MARKDOWN
            )

        if ctx.caption != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text = ctx.caption
            )

        if ctx.sticker != None:
            await self.bot.send_sticker(
                chat_id = channelChatId,
                sticker=ctx.sticker.file_id
            )

        if ctx.voice != None:
            await self.bot.send_voice(
                chat_id = channelChatId,
                voice=ctx.voice.file_id
            )

        if ctx.sticker == None and ctx.photo != None and len(ctx.photo) > 0:
            await self.bot.send_photo(
                chat_id = channelChatId,
                photo=ctx.photo[0].file_id
            )

        if ctx.video != None:
            await self.bot.send_video(
                chat_id = channelChatId,
                video=ctx.video.file_id
            )

        if ctx.document != None:
            await self.bot.send_document(
                chat_id = channelChatId,
                document=ctx.document.file_id
            )

    async def forwardMessageFromUserToManager(self, ctx: Message, channelChatId, channelChatMessageId):

        userTg = ctx.from_user

        if ctx.text != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"{userTg.full_name} @{userTg.username}:\n{ctx.text}",
                reply_to_message_id=channelChatMessageId
            )

        if ctx.caption != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"{userTg.full_name} @{userTg.username}:\n{ctx.caption}",
                reply_to_message_id=channelChatMessageId
            )

        if ctx.sticker != None:
            await self.bot.send_sticker(
                chat_id = channelChatId,
                sticker=ctx.sticker.file_id,
                reply_to_message_id=channelChatMessageId
            )

        if ctx.voice != None:
            await self.bot.send_voice(
                chat_id = channelChatId,
                voice=ctx.voice.file_id,
                reply_to_message_id=channelChatMessageId
            )

        if ctx.sticker == None and ctx.photo != None and len(ctx.photo) > 0:
            await self.bot.send_photo(
                chat_id = channelChatId,
                photo=ctx.photo[0].file_id,
                reply_to_message_id=channelChatMessageId
            )

        if ctx.video != None:
            await self.bot.send_video(
                chat_id = channelChatId,
                video=ctx.video.file_id,
                reply_to_message_id=channelChatMessageId
            )

        if ctx.document != None:
            await self.bot.send_document(
                chat_id = channelChatId,
                document=ctx.document.file_id,
                reply_to_message_id=channelChatMessageId
            )

crossDialogMessageSenderShared: CrossDialogMessageSender = None