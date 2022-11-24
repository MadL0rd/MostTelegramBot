import string
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from datetime import datetime
import json
import enum

import Core.StorageManager.StorageManager as storage
from logger import logger as log

class PageNames(enum.Enum):

    list1 = "uniqueMessages"
    ScooterCategoriesSmallList = "СкутерыМалые"
    ScooterCategoriesBigList = "СкутерыБольшие"
    MotoCategoriesList = "Мотоциклы"
    bikeCriteria = "КритерииБайка"

    onboarding = "onboarding"


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

    values = getContent(pages.list1, "A1:B200")
    if len(values) > 0:
        del values[0]

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

    values = getContent(pages.onboarding, "A1:B100")
    if len(values) > 0:
        del values[0]

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

    values = getContent(pages.bikeCriteria, "A1:Z100")
    if len(values) > 0:
        del values[0]

    content = []
    for line in values:
        criteria = {}
        criteria["type"] = line[0]
        for i in range(len(line)-1):
            criteria[f"criteria{i+1}"] = line[i+1]
        content.append(criteria)

    storage.writeJsonData(
        storage.path.botContentBikeCriteria, 
        content
    )

def updateScooterCategoriesSmallList():

    values = getContent(pages.ScooterCategoriesSmallList, "A1:A200")
    if len(values) > 0:
        del values[0]

    content = {}
    #log.debug(values)
    for line in values:
        try:
            if line[0] not in content and line[0] != "":
                content[line[0]] = line[0]
        except:
            continue

    storage.writeJsonData(
        storage.path.botContentScooterCategoriesSmallList, 
        content
    )

def updateScooterCategoriesBigList():

    values = getContent(pages.ScooterCategoriesBigList, "A1:A200")
    if len(values) > 0:
        del values[0]

    content = {}
    #log.debug(values)
    for line in values:
        try:
            if line[0] not in content and line[0] != "":
                content[line[0]] = line[0]
        except:
            continue

    storage.writeJsonData(
        storage.path.botContentScooterCategoriesBigList, 
        content
    )
def updateMotoCategoriesList():

    values = getContent(pages.MotoCategoriesList, "A1:A200")
    if len(values) > 0:
        del values[0]

    content = {}
    #log.debug(values)
    for line in values:
        try:
            if line[0] not in content and line[0] != "":
                content[line[0]] = line[0]
        except:
            continue

    storage.writeJsonData(
        storage.path.botContentMotoCategoriesList, 
        content
    )
# def updateNews():

#     values = getContent(pages.news, "A2:C100")
    
#     content = []
#     for line in values:
#         exercise = {}
#         try:
#             if line[0] != "":
#                 exercise["ID"] = line[0]
#             else: 
#                 continue
#         except:
#             continue

#         try:
#             if line[1] != "":
#                 exercise["text"] = line[1]
#         except:
#             log.debug("Argument text not found")

#         try:
#             if line[2] != "":
#                 exercise["picture"] = line[2]
#         except:
#             log.debug("Argument picture not found")            
#         content.append(exercise)

#     storage.writeJsonData(
#         storage.path.botContentNews, 
#         content
#     )

