from fastapi import BackgroundTasks, FastAPI, Header
from prepareMsg import prepareMsg
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from logger import callLogger
from datetime import datetime
from typing import Union

logFile = 'listener_' + (datetime.now()).strftime("%Y-%m-%d")+'.log'

listener = FastAPI()


class devopsPost(BaseModel):
    message: dict
    resource: dict
    createdDate: str


def callPrepareMsg(data, webhook):
    callLogger(logFile, "Iniciando preparação de mensagem")
    prepareMsg(logFile, data, webhook)


def splitWebhook(webhookHeader):
    arrayWebhookHeader = webhookHeader.split(';')
    arrayUrl = []
    for url in range(len(arrayWebhookHeader)):
        if(arrayWebhookHeader[url] != ''):
            arrayUrl.append(arrayWebhookHeader[url])

    return arrayUrl


@listener.post("/listener")
async def receive_msg(
    task: BackgroundTasks,
    devopsPost: devopsPost,
    webhook: Union[str, None] = Header(default=None, convert_underscores=False)
):
    data = jsonable_encoder(devopsPost)
    callLogger(logFile, str(data))
    webhookUrl = splitWebhook(webhook)
    task.add_task(callPrepareMsg, str(data), webhookUrl)
    return {"message": "mensagem recebida"}
