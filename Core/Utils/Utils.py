import itertools
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from logger import logger as log
import platform

isWindows = platform.system() == 'Windows'

def dictToList(source: dict):
    result = []
    for line in source:
        result.append(line)
    return result

def groupListToPairs(source: list):
    result = []
    source = source.copy()
    while len(source) > 0:
        if len(source) > 1:
            result.append([source[0], source[1]])
            del source[0]
            del source[0]
        else:
            result.append([source[0]])
            del source[0]
    return result

def replyMarkupFromListOfLines(lines: list) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    for line in lines:
        if len(line) > 1:
            keyboardMarkup.row(
                KeyboardButton(line[0]),
                KeyboardButton(line[1])
            )
        else:
            keyboardMarkup.row(
                KeyboardButton(line[0])
            )

    return keyboardMarkup

def replyMarkupFromListOfButtons(buttons: list) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    if len(buttons) > 4:
        pairs = groupListToPairs(buttons)
        return replyMarkupFromListOfLines(pairs)

    for buttonText in buttons:
        keyboardMarkup.row(
            KeyboardButton(buttonText)
        )

    return keyboardMarkup

def doubleListToButton(list1: list, list2: list, add: str, fill: str):
    # Функция пробегается одновременно по двум спискам list1 и list2
    # и формирует из них keyboardMarkup.
    # В наименьший из списков добавляет элемент add.
    # Если наименьшего нет, то добавляет один большой add в конце по центру.
    # Если после этого длины списков неодинаковы, то пробелы заполняются fill

    keyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    didAppended = False


    if len(list1) < len(list2):
        list1.append(add)
        didAppended = True
    if len(list1) > len(list2):
        list2.append(add)
        didAppended = True 
    for (item1, item2) in itertools.zip_longest(list1, list2, fillvalue= fill):
        keyboardMarkup.row(KeyboardButton(item1),KeyboardButton(item2))
    if len(list1) == len(list2) and didAppended == False:
        log.info(didAppended)
        keyboardMarkup.add(KeyboardButton(add))

    return keyboardMarkup
