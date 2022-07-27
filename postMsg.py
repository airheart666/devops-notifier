import requests
from logger import callLogger
import json


def postMsg(data, webhook):
    data = json.dumps(data)

    headersDict = {
                    'Content-Type': 'application/json',
                    'Encoding': 'utf8'
                    }
    doPost = requests.post(
                           webhook,
                           headers=headersDict,
                           data=json.loads(data).encode('utf8')
                           )

    logLine = "Realizando POST no webhook: " + webhook
    callLogger(logLine)

    postResponse = json.dumps(doPost.text, separators=(',', ': '))
    statusCode = doPost.status_code

    if(statusCode == 200):
        responseMsg = "Evento enviado com sucesso!"
        logLine = "Retorno webhook = " + postResponse
        callLogger(logLine)
    else:
        responseMsg = "Status diferente de 200, necessário validar log..."
        logLine = "Status diferente de 200:" + \
            str(statusCode) + "\nvalidar resposta: " + postResponse
        callLogger(logLine)

    return responseMsg, statusCode
