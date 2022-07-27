from fastapi import FastAPI, Header, Response
from prepareMsg import prepareMsg
import json
from pydantic import BaseModel
from logger import callLogger

listener = FastAPI()


class devopsPost(BaseModel):
    eventType: str
    resource: dict
    createdDate: str


class response(BaseModel):
    response: str
    statusWebhook: int


def splitHeader(header):
    arrayHeader = header.split(';')
    arrayElement = []
    for element in range(len(arrayHeader)):
        if(arrayHeader[element] != ''):
            arrayElement.append(arrayHeader[element])

    return arrayElement


@listener.post("/listener", response_model=response, status_code=200)
async def receive_msg(
    resposta: Response,
    devopsPost: devopsPost,
    webhook: str = Header(None),
    prefixo: str = Header(None)
):
    '''
    Endpoint POST, recebe o evento do Azure DevOps

    resposta: modelo de resposta que será devolvida ao Azure DevOps
    devopsPost: recebe o JSON do evento
    webhook: header que recebe as URL dos webhooks que serão notificados
    prefixo: header que recebe os prefixos que o Service Hook do Azure DevOps deverá monitorar
    '''
    for element in devopsPost.resource:
        value = str(devopsPost.resource.get(element))
        if(not value.startswith('{')):
            valueReplace = value.replace("'", "")
            valueDict = {element: valueReplace}
            devopsPost.resource.update(valueDict)

    data = json.dumps(devopsPost.__dict__, separators=(',', ': '))
    logLine = 'Evento recebido: ' + data
    callLogger(logLine)
    webhookUrl = splitHeader(str(webhook))
    prefixoArray = splitHeader(str(prefixo))
    #task.add_task(callPrepareMsg, str(data), webhookUrl, prefixoArray)
    response = prepareMsg(str(data), webhookUrl, prefixoArray)
    resposta.status_code = response["statusWebhook"]
    return response
