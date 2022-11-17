from aiogram import Bot, types
from aiogram.types import User, Message, ParseMode

from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.StorageManager.StorageManager as storage
from logger import logger as log

class CrossDialogMessageSender:

    bot: Bot
    waitingForOrder: dict
    orderPosts: dict
    channel: str

    def __init__(self, bot: Bot, channel: str):
        self.bot = bot
        self.waitingForOrder = {}
        self.orderPosts = {}
        self.channel = channel

    async def setWaitingForOrder(self, userTg: User, msgText):
        self.waitingForOrder[msgText] = userTg
        message = await self.bot.send_message(
            chat_id = self.channel,
            text=msgText
        )
        self.orderPosts[userTg.id] = message

    def getUserWaitingForOrder(self, text: str) -> User:
        try:
            userTg = self.waitingForOrder[text]
            return userTg
        except:
            return None

    async def makeAnOrderWithChannelChatMessageCtx(self, ctx: Message):

        channelChatId = ctx.chat.id
        channelChatMessageId = ctx.message_id
        orderId = channelChatMessageId

        text = ctx.text
        userTg = self.getUserWaitingForOrder(text)
        del self.waitingForOrder[text]
        channelMessage: Message = self.orderPosts[userTg.id]
        del self.orderPosts[userTg.id]
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

        await self.bot.send_message(
            chat_id = userTg.id,
            text=f"Заказ {orderId} успешно отправлен на обработку"
        )


    async def forwardMessageFromManagerToUser(self, ctx, order):

        channelChatId = order["userInfo"]["id"]
        orderId = order["id"]
        if ctx.text != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"*Заказ {orderId}*\n{ctx.text}",
                parse_mode=ParseMode.MARKDOWN
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

    async def forwardMessageFromUserToManager(self, ctx, channelChatId, channelChatMessageId):

        userTg = ctx.from_user

        if ctx.text != None:
            await self.bot.send_message(
                chat_id = channelChatId,
                text=f"{userTg.full_name} @{userTg.username}:\n{ctx.text}",
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