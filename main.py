import asyncio
import platform
import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery

from logger import logger as log

import MenuModules.MenuDispatcher as dispatcher
from Core.StorageManager.StorageManager import LanguageKey, StorageManager
import Core.StorageManager.StorageFactory as storageFactory
from Core.CrossDialogMessageSender import CrossDialogMessageSender, crossDialogMessageSenderShared
from Core.GoogleSheetsService import GoogleSheetsService 
import Core.Utils.Utils as utils

# =====================
# Version 1.1.3
# MostBaliBot
# https://api.telegram.org/bot5278616125:AAH65CfKVC7pCiWZyPTGQQY442l4C4tBB8E/sendMessage?chat_id=@MadL0rdTest&text=Text
# =====================

# Initialize bot and dispatcher

log.info(sys.argv)

# =====================
#       Main env
# Bot:              https://t.me/MostBaliBot
# Channel:          https://t.me/+f8yZyNqXn2piYjJi
# AllMessagesChat:  https://t.me/+SuvE0H_LmBJjMGVi
# =====================
apiKey = "5278616125:AAH65CfKVC7pCiWZyPTGQQY442l4C4tBB8E"
channel = "-1001443864958"
chat = -1001886206503
allMessagesChat = -1001505950222

# =====================
#       Test env
# Bot:              https://t.me/MadL0rdTestBot
# Channel:          https://t.me/MadL0rdTest
# AllMessagesChat:  https://t.me/+kEU20mN1KU85NWMy
# =====================

isProduction = True
if len(sys.argv) > 1 and sys.argv[1] == "-test":
    apiKey = "5769610401:AAGxxBig9ESUKUP-ctFXb9Z0iGP-9z17PVs"
    channel = "@MadL0rdTest"
    chat = -1001801213740
    allMessagesChat = -815125654
    isProduction = False

bot = Bot(token=apiKey)
dp = Dispatcher(bot)

crossDialogMessageSenderShared = CrossDialogMessageSender(bot, channel, isProduction)
crossDialogMessageSender = crossDialogMessageSenderShared

storageDefault = storageFactory.storageDefault

# =====================
# Bot commands
# =====================

@dp.message_handler(commands=['start'])
async def send_welcome_message_handler(ctx: types.Message):

    await dispatcher.handleUserStart(ctx)

@dp.message_handler(content_types=["audio", "game", "document", "photo", "sticker", "video", "voice", "video_note", "contact", "location", "venue", "invoice", "text"])
async def default_message_handler(ctx: Message):
    log.info(f"From {ctx.from_user.full_name} receive: {ctx}")
        
    # Message from private chat with user
    if ctx.chat.type == "private":

        # Forward user message to all messages chat
        await bot.forward_message(
            chat_id=allMessagesChat,
            from_chat_id=ctx.chat.id,
            message_id=ctx.message_id
        )

        userTg = ctx.from_user
        userInfo = storageDefault.getUserInfo(userTg)

        if ctx.text == "/back_to_menu" or "currentOrderDialog" not in userInfo:
            await dispatcher.handleUserMessage(ctx)
            return

        # Forward to thread in channel
        orderForDialog = userInfo["currentOrderDialog"]

        channelChatMessageId = orderForDialog["channelChatMessageId"]
        channelChatId = orderForDialog["channelChatId"]

        await crossDialogMessageSender.forwardMessageFromUserToManager(
            ctx=ctx,
            channelChatId=channelChatId,
            channelChatMessageId=channelChatMessageId
        )

    # Fetch automatic telegram message for channel order from bot
    elif ctx.from_user.first_name == "Telegram":

        # If ctx is order message from channel chat
        await crossDialogMessageSender.makeAnOrderWithChannelChatMessageCtx(ctx)
    
    # Manager message to user
    order = {}
    try:
        order = storageDefault.getOrder(ctx.reply_to_message.message_id)
    except:
        return

    await crossDialogMessageSender.forwardMessageFromManagerToUser(ctx, order)

@dp.callback_query_handler()
async def default_callback_handler(ctx: CallbackQuery):
    await dispatcher.handleCallback(ctx)

async def on_startup(_):
    crossDialogMessageSender.configureBackgroundTasks()
    asyncio.create_task(crossDialogMessageSender.threadedTasks())
    for language in LanguageKey:
        sheets = GoogleSheetsService(language)
        sheets.updateUniqueMessages()
        sheets.updateOnboarding()
        sheets.updateScooterCategoriesList()
        sheets.updateMotoCategoriesList()
        sheets.updateBikeCriteria()
    log.info("Bot just started")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

log.info("Bot just started")