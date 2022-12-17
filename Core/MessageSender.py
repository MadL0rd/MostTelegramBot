
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

from main import bot
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log
from main import bot

class MessageSender:

    async def answer(self, ctx: Message, text: str, inlineMarkup: InlineKeyboardMarkup, parse_mode=ParseMode.MARKDOWN):

        # log.debug(f"MessageSender sends: {text}")
        await ctx.answer(
            text,
            parse_mode=parse_mode,
            reply_markup=inlineMarkup
        )

    async def answer(self, ctx: Message, text: str, keyboardMarkup: ReplyKeyboardMarkup = None, parse_mode = ParseMode.MARKDOWN):
        
        # log.debug(f"MessageSender sends: {text}")
        await ctx.answer(
            text,
            parse_mode=parse_mode,
            reply_markup=keyboardMarkup
        )

    async def sendPhoto(self, ctx: Message, url: str):
        await bot.send_photo(chat_id=ctx.chat.id, photo=url)

    async def sendAudio(self, ctx: Message, url: str):
        await bot.send_voice(chat_id=ctx.chat.id, voice=url)

    async def sendVideo(self, ctx: Message, url: str):
        await bot.send_video(chat_id=ctx.chat.id, video=url)


class CallbackMessageSender(MessageSender):

    async def answer(self, ctx: Message, text: str, inlineMarkup: InlineKeyboardMarkup):

        await bot.send_message(
            chat_id=ctx.message.chat.id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inlineMarkup
        )

    async def answer(self, ctx: Message, text: str, keyboardMarkup: ReplyKeyboardMarkup):
        
        await bot.send_message(
            chat_id=ctx.message.chat.id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboardMarkup
        )

    async def answerUnknown(self, ctx: Message):

        unknownText = self.getText(textConstant.unknownState)
        await bot.send_message(
                chat_id=ctx.message.chat.id,
                text=unknownText,
                parse_mode=ParseMode.MARKDOWN
            )