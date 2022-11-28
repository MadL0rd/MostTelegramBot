from datetime import datetime, date, timedelta
from email.policy import strict
import enum
import json
from pathlib import Path
import string
import pytz
import xlsxwriter

from aiogram.types import User
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys

from logger import logger as log
import Core.Utils.Utils as utils

# =====================
# Base
# =====================

class UserHistoryEvent(enum.Enum):

    start = "Старт"
    sendMessage = "Отправил сообщение"
    callbackButtonDidTapped = "Нажал на кнопку в сообщении"
    becomeAdmin = "Стал администратором"
    startModuleOnboarding = "Начал смотреть онбординг"
    startModuleMainMenu = "Перешел в главное меню" 

    startModuleBikeCommitment = "Приступил к выбору байка"
    startModuleBikeScooterOrMoto = "Приступил к выбору скутера или мотоцикла"
    startModuleBikeMotoCategory = "Приступил к выбору категории мотоцикла"
    startModuleBikeScooterCategory = "Приступил к выбору категории скутера"
    startModuleBikeScooterCategoryChoice = "Приступил к точному указанию желаемой модели скутера"
    strartModuleBikeMotoCategoryChoice = "Приступил к точному указанию желаемой модели мотоцикла"
    startModuleBikeParameters = "Приступил к выбору параметров байка"
    startModuleBikeCriteriaChoice = "Приступил к выбору критериев"

    startModuleTimeRequest = "Приступил к выбору времени"
    startModuleTimeRequestDayWeekWhen = "Приступил к выбору даты начала аренды (длительность в днях/неделях)"
    startModuleTimeRequestDayWeekWhenSetDate = "Приступил к указанию точной даты начала аренды (длительность в днях/неделях)"
    startModuleTimeRequestHowManyDays = "Приступил к выбору длительности аренды в днях"
    startModuleTimeRequestHowManyMonths = "Приступил к выбору длительности аренды в месяцах"
    startModuleTimeRequestHowManyMonthsSet = "Приступил к указанию точного количества месяцев аренды"
    startModuletimeRequestMonthWhen = "Приступил к выбору даты начала аренды (длительность в месяцах)"
    startModuleTimeRequestMonthWhenSetDate = "Приступил к указанию точной даты начала аредны (длительность в месяцах)"

    startModuleBikeHelmet = "Приступил к выбору количества шлемов"

    startModuleRequestGeoposition = "Приступил к указанию геопозиции"
    startModuleCarSize = "Приступил к выбору размера машины"
    startModuleCarTransmission = "Приступил к выбору коробки передач"
    startModuleCarModels = "Приступил к выбору моделей"
    startModuleComment = "Приступил к написанию комментария к заказу"
class PathConfig:

    baseDir = Path("./DataStorage")
    botContentPrivateConfig = baseDir / "PrivateConfig.json"

    usersDir = baseDir / "Users"
    # userRequestFile = usersDir

    botContentDir = baseDir / "BotContent"
    botContentOnboarding = botContentDir/ "Onboarding.json"
    botContentBikeCriteria = botContentDir/ "BikeCriteria.json"
    botContentUniqueMessages = botContentDir/ "UniqueTextMessages.json"
    totalHistoryTableFile = baseDir / "TotalHistory.xlsx"
    statisticHistoryTableFile = baseDir / "StatisticalHistory.xlsx"
    botContentScooterCategoriesSmallList = botContentDir / "ScooterCategoriesSmall.json"
    botContentScooterCategoriesBigList = botContentDir / "ScooterCategoriesBig.json"
    botContentMotoCategoriesList = botContentDir / "MotoCategories.json"

    channelOrdersDir = baseDir / "Orders"

    def orderDir(self, orderId: int):
        return self.channelOrdersDir / f"{orderId}.json"

    def userFolder(self, user: User):
        return self.usersDir / f"{user.id}"

    def userInfoFile(self, user: User):
        return self.userFolder(user) / "info.json"
    
    def userRequestFile(self, user: User):
        return self.userFolder(user) / "request.json"

    def userHistoryFile(self, user: User):
        return self.userFolder(user) / "history.json"

path = PathConfig()

def getJsonData(filePath: Path):
    with filePath.open() as json_file:
        data = json.load(json_file)
    return data

def writeJsonData(filePath: Path, content):
    # log.debug(content)
    if utils.isWindows:
        data = json.dumps(content, indent=2)
        with filePath.open('w', encoding= 'utf-8') as file:
            file.write(data)
    else:
        data = json.dumps(content, ensure_ascii=False, indent=2)
        with filePath.open('w') as file:
            file.write(data)

# =====================
# Public interaction
# =====================


def getOrder(orderId: int) -> dict:
    orderFile = path.orderDir(orderId)

    # If user file does not exist
    if not orderFile.exists():
        log.info(f"Order {orderId} file does not exist")
        updateOrderData(orderId, {})
        return {}
    
    return getJsonData(orderFile)

def updateOrderData(orderId: int, data: dict):
    
    orderFile = path.orderDir(orderId)
    data["updateTime"] = getTimestamp()
    writeJsonData(orderFile, data)

def getUserInfo(user: User):
    
    userInfoFile = path.userInfoFile(user)

    # If user file does not exist
    if not userInfoFile.exists():
        log.info(f"User {user.id} dir does not exist")
        generateUserStorage(user)

    userInfoFile = path.userInfoFile(user)

    return getJsonData(userInfoFile)

def getUserRequest(user: User)->list: 
    
    userRequestFile = path.userRequestFile(user)

    # If user file does not exist
    if not userRequestFile.exists():
        log.info(f"User {user.id} dir does not exist")
        generateUserStorage(user)

    userRequestFile = path.userRequestFile(user)

    return getJsonData(userRequestFile)

def logToUserRequest(user: User, codingKey: RequestCodingKeys, text: str):
    request = getUserRequest(user)
    log.info(type(request))
    request[codingKey.get] = text
    updateUserRequest(user, request)

def generateUserStorage(user: User):

    userFolder = path.userFolder(user)
    userFolder.mkdir(parents=True, exist_ok=True)

    # notoficationsConfig = getJsonData(path.botContentNotificationTimes)
    
    userData = json.loads(user.as_json())
    userData = {
        "info": userData,
        "isAdmin": False,
        "state": {},
        # "notifications": notoficationsConfig["userDefault"]
    }
    updateUserRequest(user,[])
    updateUserData(user, userData)
    logToUserHistory(user, UserHistoryEvent.start, "Начало сохранения истории пользователя")

def getTimestamp():

    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    return {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M:%S"),
        "week": now.isocalendar()[1]
    }

def updateUserData(user: User, userData):
    
    userInfoFile = path.userInfoFile(user)
    userData["updateTime"] = getTimestamp()
    writeJsonData(userInfoFile, userData)

def updateUserRequest(user: User, userRequest):
    
    userRequestFile = path.userRequestFile(user)
    writeJsonData(userRequestFile, userRequest)

def logToUserHistory(user: User, event: UserHistoryEvent, content: string):

    log.info(f"{user.id} {event.value}: {content}")

    historyFile = path.userHistoryFile(user)

    history = []
    if historyFile.exists():
        history = getJsonData(historyFile)
    
    history.append({
        "timestamp": getTimestamp(),
        "event": event.value,
        "content": content
    })

    writeJsonData(historyFile, history)

# =====================
# Data tables creation
# =====================

def generateStatisticTable():

    log.info("Statistic table generation start")

    statisticEvents = [
        UserHistoryEvent.start
    ]

    dateConfig = getJsonData(path.botContentPrivateConfig)["startDate"]
    startDate = date(dateConfig["year"], dateConfig["month"], dateConfig["day"])
    
    workbook = xlsxwriter.Workbook(path.statisticHistoryTableFile)

    # event = UserHistoryEvent.assessmentDelta
    # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.sum)

    # event = UserHistoryEvent.assessmentBefore
    # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)
    # event = UserHistoryEvent.assessmentAfter
    # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)

    for event in statisticEvents:
        generateStatisticPageForEvent(workbook, event.value, startDate)

    workbook.close()

    log.info("Statistic table generation completed")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

class StatisticPageOperation(enum.Enum):
    count = "Количество"
    sum = "Сумма"
    average = "Среднее значение"

def generateStatisticPageForEvent(workbook: xlsxwriter.Workbook, eventName: string, startDate: date, operation: StatisticPageOperation = StatisticPageOperation.count):

    worksheet = workbook.add_worksheet(eventName)
    row = 1
    col = 0

    startRow = 4

    worksheet.write(row, col, "Метрика:")
    worksheet.write(row, col + 1, eventName)
    row += 1
    worksheet.write(row, col, "Тип агрегирования:")
    worksheet.write(row, col + 1, operation.value)

    row = startRow
    worksheet.write(row, col, "Дата / Пользователь")
    row += 1

    dates = [strDate.strftime("%d.%m.%Y") for strDate in daterange(startDate, date.today())]
    for single_date in dates:
        worksheet.write(row, col, single_date)
        row += 1
    col += 1

    usersCount = 0
    for userFolder in path.usersDir.iterdir():
        usersCount += 1
        row = startRow
        history = getJsonData(userFolder / "history.json")
        
        columnTitle = f"user{userFolder.name}"
        worksheet.write(row, col, columnTitle)
        
        row += 1
        for single_date in dates:
            dayEvents = [event for event in history if event["timestamp"]["date"] == single_date and event["event"] == eventName]

            if operation == StatisticPageOperation.count:
                dateEventsCount = len(dayEvents)
                worksheet.write(row, col, dateEventsCount)

            if operation == StatisticPageOperation.sum:
                try:
                    values = [int(event["content"]) for event in dayEvents]
                except:
                    values = []
                worksheet.write(row, col, sum(values))

            if operation == StatisticPageOperation.average:
                try:
                    values = [int(event["content"]) for event in dayEvents]
                    result = sum(values) / len(values)
                except:
                    result = 0
                worksheet.write(row, col, result)

            row += 1

        col += 1

    worksheet.set_column(0, usersCount, 15)

def generateTotalTable():
    log.info("Total table generation start")

    workbook = xlsxwriter.Workbook(path.totalHistoryTableFile)
    bold = workbook.add_format({'bold': True})

    for userFolder in path.usersDir.iterdir():
        sheetTitle = f"user{userFolder.name}"
        
        worksheet = workbook.add_worksheet(sheetTitle)
        row = 0 

        titles = ["Дата", "Время", "Неделя", "Событие", "Описание"]
        for col, title in enumerate(titles):
            worksheet.write(row, col, title, bold)
            worksheet.set_column(col, col, len(title))
        worksheet.set_column(4, 4, 50)

        history = getJsonData(userFolder / "history.json")

        row = 1
        for event in history:
            col = 0
            worksheet.write(row, col, event["timestamp"]["date"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["time"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["week"])
            col += 1
            worksheet.write(row, col, event["event"])
            col += 1
            worksheet.write(row, col, event["content"])
            row += 1

    workbook.close()

    log.info("Total table generation completed")