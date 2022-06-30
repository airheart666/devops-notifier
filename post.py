import requests
from logger import callLogger
import json


def postMsg(logFile, data, webhook):
    reqUrl = webhook

    data = json.dumps(data)

    headers_dict = {
                    'Content-Type': 'application/json',
                    'Encoding': 'utf8'
                    }

    doPost = requests.post(
                       reqUrl,
                       headers=headers_dict,
                       data=json.loads(data).encode('utf8')
                       )

    callLogger(logFile, "Enviando")

    retorno = doPost.text

    callLogger(logFile, retorno)

    return retorno
