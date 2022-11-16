def groupButtonsToPairs(source: list):
    result = []
    while len(source) > 0:
        if len(source) > 1:
            result.append([source[0], source[1]])
            del source[0]
            del source[0]
        else:
            result.append([source[0]])
            del source[0]
    return result

noNotificationText = "Не отправлять"

def replyMarkupForNotificationType(type: str) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    notoficationTimes = storage.getJsonData(storage.path.botContentNotificationTimes)[type]
    notoficationTimes.append(noNotificationText)
    notoficationTimes = groupButtonsToPairs(notoficationTimes)
    for line in notoficationTimes:
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