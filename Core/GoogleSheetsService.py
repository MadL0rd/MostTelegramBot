import string
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import enum

from Core.StorageManager.StorageManager import LanguageKey, StorageManager
from logger import logger as log

class PageNames(enum.Enum):

    uniqueMessages = "УникальныеСообщения"
    scooterCategoriesList = "Скутеры"
    motoCategoriesList = "Мотоциклы"
    bikeCriteria = "КритерииБайкаV2"
    onboarding = "Онбординг"

pages = PageNames

CREDENTIALS_FILE = 'creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
)
httpAuth = credentials.authorize(httplib2.Http())

service = build('sheets', 'v4', http = httpAuth)
service_drive = build('drive', 'v3', http = httpAuth)

spreadsheetIds = {
    LanguageKey.ru.value: '1qHfbOZiUaS4Ztr2yveBM0M0r1TGo9Vadw2IZYJWNlA8',
    LanguageKey.en.value: '12JwUbAgE-AJnF6aAKWiaSGxPPWJQ-WKX2wegxWFsX3Y'
}

class GoogleSheetsService:

    languageKey: str
    spreadsheetId: str
    storage: StorageManager

    def __init__(self, language: LanguageKey):
        self.languageKey = language.value
        self.spreadsheetId = spreadsheetIds[language.value]
        self.storage =  StorageManager(language)

    def getTableModifiedTime(self):
        response = service_drive.files().get(fileId=self.spreadsheetId,fields="modifiedTime").execute()
        modified_time_str = response['modifiedTime']
        date = datetime.fromisoformat(modified_time_str[:-1])
        return date

    def getContent(self, page: PageNames, range: string):
        values = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId,
            range=f'{page.value}!{range}',
            majorDimension='ROWS'
        ).execute()

        values = values['values']
        return values

    def updateUniqueMessages(self):

        values = self.getContent(pages.uniqueMessages, "A2:B200")

        content = {}
        #log.debug(values)
        for line in values:
            try:
                if line[0] not in content and line[0] != "":
                    content[line[0]] = line[1]
            except:
                continue

        self.storage.writeJsonData(
            self.storage.path.botContentUniqueMessages, 
            content
        )
        
    def updateOnboarding(self):

        values = self.getContent(pages.onboarding, "A2:B100")

        content = []
        for line in values:
            content.append({
                "message": line[0],
                "buttonText": line[1]
            })

        self.storage.writeJsonData(
            self.storage.path.botContentOnboarding, 
            content
        )

    def updateBikeCriteria(self):

        values = self.getContent(pages.bikeCriteria, "A2:Z100")

        content = []
        for line in values:
            criteria = {}
            criteria["id"] = line[0]
            del line[0]
            criteria["title"] = line[0]
            del line[0]
            criteria["question"] = line[0]
            del line[0]
            criteria["customTextEnable"] = line[0] == "TRUE"
            del line[0]
            criteria["bikes"] = line[0].split("\n")
            del line[0]
            criteria["values"] = line
            content.append(criteria)

        self.storage.writeJsonData(
            self.storage.path.botContentBikeCriteria, 
            content
        )

    def updateScooterCategoriesList(self):

        values = self.getContent(pages.scooterCategoriesList, "A2:B200")

        contentSmall = list()
        contentBig = list()
        #log.debug(values)
        for line in values:
            try:
                if line[0] not in contentSmall and line[0] != "":
                    contentSmall.append(line[0])
                if line[1] not in contentBig and line[1] != "":
                    contentBig.append(line[1])
            except:
                continue

        self.storage.writeJsonData(
            self.storage.path.botContentScooterCategoriesSmallList, 
            contentSmall
        )
        self.storage.writeJsonData(
            self.storage.path.botContentScooterCategoriesBigList, 
            contentBig
        )

    def updateMotoCategoriesList(self):

        values = self.getContent(pages.motoCategoriesList, "A2:A200")

        content = list()
        #log.debug(values)
        for line in values:
            try:
                if line[0] not in content and line[0] != "":
                    content.append(line[0])
            except:
                continue

        self.storage.writeJsonData(
            self.storage.path.botContentMotoCategoriesList, 
            content
        )