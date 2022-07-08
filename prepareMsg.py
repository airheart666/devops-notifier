from postMsg import postMsg
from logger import callLogger
from eventHandler import eventSwitcher
import json


def prepareMsg(logFile, data, webhook, prefix):

    data = data.replace("'", '"')
    jsonData = json.loads(data)

    eventType = jsonData["eventType"]
    repo = jsonData["resource"]["repository"]["name"]

    if(eventType == 'git.pullrequest.updated'):
        statusDict = {
                        'completed': 'completed',
                        'abandoned': 'abandoned'
                    }

        pullStatus = jsonData["resource"]["status"]
        eventType = eventType + '.' + statusDict[pullStatus]

    eventMsg = eventSwitcher(logFile, eventType, jsonData)
    print(eventMsg)
    msg = "{\"text\":\"" + eventMsg + "\"}"

    callLogger(logFile, "Iniciando envio")

    if(repo.startswith(prefix)):
        for url in range(len(webhook)):
            post = postMsg(logFile, msg, webhook[url])

        return post
