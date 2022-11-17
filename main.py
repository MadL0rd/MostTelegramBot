import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery
from Core.GoogleSheetsService import UpdateMotoCategoriesList, UpdateScooterCategoriesBigList, UpdateScooterCategoriesSmallList, updateOnboarding, updateUniqueMessages

from logger import logger as log

import MenuModules.MenuDispatcher as dispatcher
import Core.StorageManager.StorageManager as storage
from Core.CrossDialogMessageSender import CrossDialogMessageSender, crossDialogMessageSenderShared

# =====================
# Version 0.1.0
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
allMessagesChat = -721123169

# =====================
#       Test env
# Bot:              https://t.me/MadL0rdTestBot
# Channel:          https://t.me/MadL0rdTest
# AllMessagesChat:  https://t.me/+kEU20mN1KU85NWMy
# =====================
if len(sys.argv) > 1 and sys.argv[1] == "-test":
    apiKey = "5769610401:AAGxxBig9ESUKUP-ctFXb9Z0iGP-9z17PVs"
    channel = "@MadL0rdTest"
    chat = -1001801213740
    allMessagesChat = -815125654

bot = Bot(token=apiKey)
dp = Dispatcher(bot)

crossDialogMessageSenderShared = CrossDialogMessageSender(bot, channel)
crossDialogMessageSender = crossDialogMessageSenderShared

# =====================
# Bot commands
# =====================

@dp.message_handler(commands=['start'])
async def send_welcome_message_handler(ctx: types.Message):

    await dispatcher.handleUserStart(ctx)

    # Here is test post creation
    userTg = ctx.from_user
    msgText = f"Created an order for {userTg.full_name} @{userTg.username}"
    await crossDialogMessageSender.setWaitingForOrder(userTg, msgText)

@dp.message_handler(content_types=["text", "sticker", "voice", "photo", "audio", "video", "document"])
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
        userInfo = storage.getUserInfo(userTg)

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

    if ctx.chat.id != chat:
        return

    # Fetch automatic telegram message for channel order from bot
    elif ctx.from_user.first_name == "Telegram":

        # If ctx is order message from channel chat
        if crossDialogMessageSender.getUserWaitingForOrder(ctx.text) == None:
            return
        await crossDialogMessageSender.makeAnOrderWithChannelChatMessageCtx(ctx)        
    
    # Manager message to user
    order = {}
    try:
        order = storage.getOrder(ctx.reply_to_message.message_id)
    except:
        return

    await crossDialogMessageSender.forwardMessageFromManagerToUser(ctx, order)


@dp.callback_query_handler()
async def default_callback_handler(ctx: CallbackQuery):
    await dispatcher.handleCallback(ctx)

async def on_startup(_):
    updateUniqueMessages()
    updateOnboarding()
    UpdateScooterCategoriesSmallList()
    UpdateScooterCategoriesBigList()
    UpdateMotoCategoriesList()
    print("LETS GO")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

log.info("Bot just started")