import requests
import time

from logger import logger as log

def currentMilliTime():
    return round(time.time() * 1000)

def createCard(title: str, description: str):

    startTime = currentMilliTime()

    url = "https://api.trello.com/1/cards"

    headers = {
    "Accept": "application/json"
    }

    query = {
        "key": "7cdb883b54cfa75f2b016922ed481a7f",
        "token": "4debfd8b041f59fc21f7090dd27440859c278376b41b6659ff8119af55b71f3b",
        "idList": "637c98853662f80248211a4e",
        "name": title,
        "desc": description,
        "start": startTime,
        "pos": "top"
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )
    log.info(f"Trello card creation status code: {response.status_code}")