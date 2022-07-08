from fastapi import BackgroundTasks, FastAPI, Header
from prepareMsg import prepareMsg
import json
from pydantic import BaseModel
from logger import callLogger
from datetime import datetime

logFile = 'listener_' + (datetime.now()).strftime("%Y-%m-%d")+'.log'

listener = FastAPI()


class devopsPost(BaseModel):
    eventType: str
    message: dict
    detailedMessage: dict
    resource: dict
    createdDate: str


def callPrepareMsg(data, webhook, prefix):
    callLogger(logFile, "PREPARANDO MENSAGEM")
    prepareMsg(logFile, data, webhook, prefix)


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
    webhook: str = Header(None),
    prefix: str = Header(None)
):
    data = json.dumps(devopsPost.__dict__, indent=4)
    callLogger(logFile, str(data))
    webhookUrl = splitWebhook(webhook)
    task.add_task(callPrepareMsg, str(data), webhookUrl, prefix)
    return {"message": "evento recebido"}
