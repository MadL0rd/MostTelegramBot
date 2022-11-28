import asyncio
import aioschedule
from aiogram import Bot, types
from aiogram.types import User, Message, ParseMode

from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.StorageManager.StorageManager as storage
import Core.TrelloService as trello
from logger import logger as log

class OrderCreationEntities:

    # userLoadingMessage: Message = None
    user: User = None
    channelPost: Message = None
    treloCardId: int

    def __init__(
        self,
        # userLoadingMessage: Message,
        user: User,
        channelPost: Message,
        treloCardId: int
    ):
        # self.userLoadingMessage = userLoadingMessage
        self.user = user
        self.channelPost = channelPost
        self.treloCardId = treloCardId

orderCreationEntities = {}
telegramServiceMessagesToReply = {}

class CrossDialogMessageSender:

    bot: Bot
    channel: str

    def __init__(self, bot: Bot, channel: str):
        self.bot = bot
        self.channel = channel

    def configureBackgroundTasks(self):
        aioschedule.every(5).seconds.do(self.orderCreationRegularTask)

    async def threadedTasks(self):
        log.info("Tasks thread start")
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)

    async def setWaitingForOrder(self, userTg: User, msgText):
        message = await self.bot.send_message(
            chat_id = self.channel,
            text=msgText
        )

        # TODO: implement test env to evoid terllo card creation while testing
        response = trello.createCard(
            title = f"@{userTg.username}",
            description = msgText
        )
        orderCreationEntities[message.text] = OrderCreationEntities(
            user = userTg,
            channelPost = message,
            treloCardId=response["id"]
        )

    async def makeAnOrderWithChannelChatMessageCtx(self, ctx: Message):
        telegramServiceMessagesToReply[ctx.text] = ctx

    async def orderCreationRegularTask(self):
        log.info(f"len orderCreationEntities: {len(orderCreationEntities)}; len telegramServiceMessagesToReply: {len(telegramServiceMessagesToReply)}")

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
                text=f"*id{orderId}*\n{text}",
                parse_mode=ParseMode.MARKDOWN
            )

            orderData = {
                "id": orderId,
                "channelMessageId": channelMessage.message_id,
                "channelChatId": channelChatId,
                "channelChatMessageId": channelChatMessageId,
                "status": "Создан",
                "trelloCardId": orderCreationEntity.treloCardId,
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