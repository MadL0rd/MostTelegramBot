import Core.StorageManager.StorageManager as storage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, User

def dictToList(source: dict):
    result = []
    for line in source:
        result.append(line)
    return result
