import string
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import enum

import Core.StorageManager.StorageManager as storage
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

spreadsheet_id = '1qHfbOZiUaS4Ztr2yveBM0M0r1TGo9Vadw2IZYJWNlA8'

def getTableModifiedTime():
    response = service_drive.files().get(fileId=spreadsheet_id,fields="modifiedTime").execute()
    modified_time_str = response['modifiedTime']
    date = datetime.fromisoformat(modified_time_str[:-1])
    return date

def getContent(page: PageNames, range: string):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{page.value}!{range}',
        majorDimension='ROWS'
    ).execute()

    values = values['values']
    return values

def updateUniqueMessages():

    values = getContent(pages.uniqueMessages, "A2:B200")

    content = {}
    #log.debug(values)
    for line in values:
        try:
            if line[0] not in content and line[0] != "":
                content[line[0]] = line[1]
        except:
            continue

    storage.writeJsonData(
        storage.path.botContentUniqueMessages, 
        content
    )
    
def updateOnboarding():

    values = getContent(pages.onboarding, "A2:B100")

    content = []
    for line in values:
        content.append({
            "message": line[0],
            "buttonText": line[1]
        })

    storage.writeJsonData(
        storage.path.botContentOnboarding, 
        content
    )

def updateBikeCriteria():

    values = getContent(pages.bikeCriteria, "A2:Z100")

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

    storage.writeJsonData(
        storage.path.botContentBikeCriteria, 
        content
    )

def updateScooterCategoriesList():

    values = getContent(pages.scooterCategoriesList, "A2:B200")

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

    storage.writeJsonData(
        storage.path.botContentScooterCategoriesSmallList, 
        contentSmall
    )
    storage.writeJsonData(
        storage.path.botContentScooterCategoriesBigList, 
        contentBig
    )

def updateMotoCategoriesList():

    values = getContent(pages.motoCategoriesList, "A2:A200")

    content = list()
    #log.debug(values)
    for line in values:
        try:
            if line[0] not in content and line[0] != "":
                content.append(line[0])
        except:
            continue

    storage.writeJsonData(
        storage.path.botContentMotoCategoriesList, 
        content
    )