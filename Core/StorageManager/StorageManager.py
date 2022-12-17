from datetime import datetime, date, timedelta
from email.policy import strict
import enum
import json
from pathlib import Path
import string
import pytz
import xlsxwriter

from aiogram.types import User
from Core.StorageManager.UniqueMessagesKeys import UniqueMessagesKeys
from Core.StorageManager.LanguageKey import LanguageKey
from Core.StorageManager.PathConfig import PathConfig
from Core.StorageManager.UserHistoryEvent import UserHistoryEvent
import Core.Utils.Utils as utils

from logger import logger as log

class StatisticPageOperation(enum.Enum):
    count = "Количество"
    sum = "Сумма"
    average = "Среднее значение"

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

def getTimestamp():

    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    return {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M:%S"),
        "week": now.isocalendar()[1]
    }

class StorageManager:

    languageKey: str
    path: PathConfig

    def __init__(self, language: LanguageKey):
        self.languageKey = language.value
        self.path = PathConfig(language)

    def getJsonData(self, filePath: Path):
        with filePath.open() as json_file:
            data = json.load(json_file)
        return data

    def writeJsonData(self, filePath: Path, content):
        # log.debug(content)
        if utils.isWindows:
            data = json.dumps(content, indent=2)
            with filePath.open('w', encoding= 'utf-8') as file:
                file.write(data)
        else:
            data = json.dumps(content, ensure_ascii=False, indent=2)
            with filePath.open('w') as file:
                file.write(data)

    def getTextConstant(self, messageKey: UniqueMessagesKeys) -> str:
        messagesKeysValues = self.getJsonData(self.path.botContentUniqueMessages)
        if messageKey.value in messagesKeysValues:
            return messagesKeysValues[messageKey.value]
        else:
            return "Unknown"

    def getAndReplaceOrderMaskWith(self, messageKey: UniqueMessagesKeys, text: str) -> str:
        messagesKeys = self.getJsonData(self.path.botContentUniqueMessages)
        if messageKey.value in messagesKeys:
            value: str = messagesKeys[messageKey.value]
            mask: str = self.getTextConstant(UniqueMessagesKeys.orderNumberMask)
            return value.replace(mask, text)
        else:
            return "Unknown"

    def getOrder(self, orderId: int) -> dict:
        orderFile = self.path.orderDir(orderId)

        # If user file does not exist
        if not orderFile.exists():
            log.info(f"Order {orderId} file does not exist")
            self.updateOrderData(orderId, {})
            return {}
        
        return self.getJsonData(orderFile)

    def updateOrderData(self, orderId: int, data: dict):
        
        orderFile = self.path.orderDir(orderId)
        data["updateTime"] = getTimestamp()
        self.writeJsonData(orderFile, data)

    def getUserInfo(self, user: User):
        
        userInfoFile = self.path.userInfoFile(user)

        # If user file does not exist
        if not userInfoFile.exists():
            log.info(f"User {user.id} dir does not exist")
            self.generateUserStorage(user)

        userInfoFile = self.path.userInfoFile(user)

        return self.getJsonData(userInfoFile)

    def getUserRequest(self, user: User)->list: 
        
        userRequestFile = self.path.userRequestFile(user)

        # If user file does not exist
        if not userRequestFile.exists():
            log.info(f"User {user.id} dir does not exist")
            self.generateUserStorage(user)

        userRequestFile = self.path.userRequestFile(user)

        return self.getJsonData(userRequestFile)

    def logToUserRequest(self, user: User, codingKey: UniqueMessagesKeys, value: str):
        request = self.getUserRequest(user)
        log.info(type(request))
        request[codingKey.value] = {
            "title": self.getTextConstant(codingKey),
            "value": value
        }
        self.updateUserRequest(user, request)

    def logToUserRequestCustom(self, user: User, codingKey: str, title: str, value: str):
        request = self.getUserRequest(user)
        log.info(type(request))
        request[codingKey] = {
            "title": title,
            "value": value
        }
        self.updateUserRequest(user, request)

    def generateUserStorage(self, user: User):

        userFolder = self.path.userFolder(user)
        userFolder.mkdir(parents=True, exist_ok=True)
        
        userData = json.loads(user.as_json())
        userData = {
            "info": userData,
            "isAdmin": False,
            "state": {},
            "language": user.language_code
        }
        self.updateUserRequest(user,[])
        self.updateUserData(user, userData)
        self.logToUserHistory(user, UserHistoryEvent.start, "Начало сохранения истории пользователя")

    def updateUserData(self, user: User, userData):
        
        userInfoFile = self.path.userInfoFile(user)
        userData["updateTime"] = getTimestamp()
        self.writeJsonData(userInfoFile, userData)

    def updateUserRequest(self, user: User, userRequest):
        
        userRequestFile = self.path.userRequestFile(user)
        self.writeJsonData(userRequestFile, userRequest)

    def logToUserHistory(self, user: User, event: UserHistoryEvent, content: string):

        log.info(f"{user.id} {event.value}: {content}")

        historyFile = self.path.userHistoryFile(user)

        history = []
        if historyFile.exists():
            history = self.getJsonData(historyFile)
        
        history.append({
            "timestamp": getTimestamp(),
            "event": event.value,
            "content": content
        })

        self.writeJsonData(historyFile, history)

    # =====================
    # Data tables creation
    # =====================

    def generateStatisticTable(self):

        log.info("Statistic table generation start")

        statisticEvents = [
            UserHistoryEvent.start
        ]

        dateConfig = self.getJsonData(self.path.botContentPrivateConfig)["startDate"]
        startDate = date(dateConfig["year"], dateConfig["month"], dateConfig["day"])
        
        workbook = xlsxwriter.Workbook(self.path.statisticHistoryTableFile)

        # event = UserHistoryEvent.assessmentDelta
        # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.sum)

        # event = UserHistoryEvent.assessmentBefore
        # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)
        # event = UserHistoryEvent.assessmentAfter
        # generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)

        for event in statisticEvents:
            self.generateStatisticPageForEvent(workbook, event.value, startDate)

        workbook.close()

        log.info("Statistic table generation completed")

    def generateStatisticPageForEvent(self, workbook: xlsxwriter.Workbook, eventName: string, startDate: date, operation: StatisticPageOperation = StatisticPageOperation.count):

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
        for userFolder in self.path.usersDir.iterdir():
            usersCount += 1
            row = startRow
            history = self.getJsonData(userFolder / "history.json")
            
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

    def generateTotalTable(self):
        log.info("Total table generation start")

        workbook = xlsxwriter.Workbook(self.path.totalHistoryTableFile)
        bold = workbook.add_format({'bold': True})

        for userFolder in self.path.usersDir.iterdir():
            sheetTitle = f"user{userFolder.name}"
            
            worksheet = workbook.add_worksheet(sheetTitle)
            row = 0 

            titles = ["Дата", "Время", "Неделя", "Событие", "Описание"]
            for col, title in enumerate(titles):
                worksheet.write(row, col, title, bold)
                worksheet.set_column(col, col, len(title))
            worksheet.set_column(4, 4, 50)

            history = self.getJsonData(userFolder / "history.json")

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