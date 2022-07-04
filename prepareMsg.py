from postMsg import postMsg
from logger import callLogger
from eventHandler import eventSwitcher
import json


def prepareMsg(logFile, data, webhook):

    data = data.replace("'", '"')
    jsonData = json.loads(data)

    eventType = jsonData["eventType"]

    eventMsg = eventSwitcher(logFile, eventType, jsonData)
    print(eventMsg)
    msg = "{\"text\":\"" + eventMsg + "\"}"

    callLogger(logFile, "Iniciando envio")

    for url in range(len(webhook)):
        post = postMsg(logFile, msg, webhook[url])

    return post
