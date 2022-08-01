from postMsg import postMsg
from logger import callLogger
from eventHandler import eventSwitcher
import json


def prepareMsg(data, webhook, prefixo):
    '''
    Função que faz o tratamento inicial do JSON do evento, antes de passar para o handler que trata cada tipo de evento mapeado, e envia a mensagem pronta para a funçãpo postMsg, que realiza o post no webhook do chat
    '''
    data = data.replace("'", '"')
    jsonData = json.loads(data)

    eventType = jsonData["eventType"]
    repo = jsonData["resource"]["repository"]["name"]

    if(eventType == 'git.pullrequest.updated'):
        statusDict = {
                        'completed': 'completed',
                        'abandoned': 'abandoned',
                        'active': 'active'
                    }

        pullStatus = jsonData["resource"]["status"]
        eventType = eventType + '.' + statusDict[pullStatus]

    logLine = "Evento = " + eventType
    callLogger(logLine)

    eventMsg = eventSwitcher(eventType, jsonData)
    msg = "{\"text\":\"" + eventMsg + "\"}"

    logLine = "Iniciando envio: " + msg
    callLogger(logLine)

    for element in range(len(prefixo)):
        logLine = 'Checando prefixo: ' + str(prefixo[element])
        callLogger(logLine)
        if(repo.startswith(prefixo[element])):
            for url in range(len(webhook)):
                responseMsg, responseStatus = postMsg(msg, webhook[url])
                response = {
                    "response": responseMsg,
                    "statusWebhook": responseStatus
                }
        else:
            logLine = 'Repositório não possui o prefixo ' + \
                str(prefixo[element])
            callLogger(logLine)
            response = {
                "response": "repo não possui o prefixo correto para este hook",
                "statusWebhook": 200
                }

    return response
