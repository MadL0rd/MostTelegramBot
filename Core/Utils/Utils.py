from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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