import asyncio
import aioschedule
from aiogram import Bot
from aiogram.types import User, Message, ParseMode
import time

from Core.StorageManager.UniqueMessagesKeys import UniqueMessagesKeys as textConstant
import Core.StorageManager.StorageFactory as storageFactory
import Core.TrelloService as trello

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
sleepTime = 5

class CrossDialogMessageSender:

    bot: Bot
    channel: str
    needToCreateTrelloCard: bool

    def __init__(self, bot: Bot, channel: str, needToCreateTrelloCard: bool):
        self.bot = bot
        self.channel = channel
        self.needToCreateTrelloCard = needToCreateTrelloCard

    def configureBackgroundTasks(self):
        aioschedule.every(sleepTime).seconds.do(self.orderCreationRegularTask)

    async def threadedTasks(self):
        log.info("Tasks thread start")
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(sleepTime)

    async def setWaitingForOrder(self, userTg: User, msgText: str):

        language = storageFactory.getLanguageForUser(userTg)
        storage = storageFactory.getStorageForLanguage(language)

        msgText = f"{language.value}\n{msgText}"
        
        message = await self.bot.send_message(
            chat_id = self.channel,
            text = msgText,
            parse_mode = ParseMode.HTML
        )

        userRequest = storage.getUserRequest(userTg)
        bikeName = "None"
        if textConstant.bikeMotoCategory.value in userRequest:
            bikeName = userRequest[textConstant.bikeMotoCategory.value]["value"]
        if textConstant.bikeScooterCategory.value in userRequest:
            bikeName = userRequest[textConstant.bikeScooterCategory.value]["value"]

        trelloCardTitle = f"@{userTg.username}: {bikeName}"
        response = { 
            "id": None
        }
        if self.needToCreateTrelloCard == True:
            response = trello.createCard(
                title = trelloCardTitle,
                description = f"https://t.me/{userTg.username}\n{msgText}"
            )
        
        orderCreationEntities[message.text] = OrderCreationEntities(
            user = userTg,
            channelPost = message,
            treloCard = {
                "id": response["id"],
                "title": trelloCardTitle
            },
            userRequest = userRequest
        )

    async def makeAnOrderWithChannelChatMessageCtx(self, ctx: Message):
        telegramServiceMessagesToReply[ctx.text] = ctx

    async def orderCreationRegularTask(self):
        aioschedule.clear()
        while True:
            await asyncio.sleep(sleepTime)

            if len(telegramServiceMessagesToReply) == 0:
                continue

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
            try:
                newText = f"<b>id{orderId}</b>\n{text}"
                await channelMessage.edit_text(
                    text=newText,
                    parse_mode=ParseMode.HTML
                )
            except:
                log.error("ChannelMessage order text already updated!")
                continue

            text = messageText
            userTg = orderCreationEntity.user
            channelMessage: Message = orderCreationEntity.channelPost
            try:
                newText = f"<b>id{orderId}</b> - {text}"
                await channelMessage.edit_text(
                    text=newText,
                    parse_mode=ParseMode.HTML
                )
            except:
                log.error("ChannelMessage order text already updated!")
                continue

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

            storage = storageFactory.getStorageForUser(userTg)
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

            text = storage.getAndReplaceOrderMaskWith(textConstant.orderCreationUserText, f'{orderId}')
            await self.bot.send_message(
                chat_id = userTg.id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )

            if orderCreationEntity.treloCard["id"] != None:
                trello.updateCardTitle(
                    id=orderCreationEntity.treloCard["id"],
                    title=f"id{orderId} {orderCreationEntity.treloCard['title']}"
                )

            del orderCreationEntities[messageText]
            del telegramServiceMessagesToReply[messageText]

    async def forwardMessageFromManagerToUser(self, ctx, order):

        channelChatId = order["userInfo"]["id"]
        storage = storageFactory.getStorageForUser(channelChatId)
        orderId = order["id"]

        text = storage.getAndReplaceOrderMaskWith(textConstant.orderDetailsMessageTitle, f'{orderId}')
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