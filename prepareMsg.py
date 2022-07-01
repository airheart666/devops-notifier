from post import postMsg
from logger import callLogger
import json

def eventSwitcher(logFile, eventType, data):

        switcher = {
            "git.push": trataCodePushed,
            "git.pullrequest.created": trataPullRequest
        }
        msg = switcher[eventType](logFile, data)
        return msg

def prepareMsg(logFile, data, webhook):

    data = data.replace("'", '"')
    jsonData = json.loads(data)

    eventType = jsonData["eventType"]

    print(eventType)

    #if(eventType == "git.push"):
    #    autor = jsonData["resource"]["pushedBy"]["displayName"]
    #elif (eventType == "git.pullrequest.created"):
    #     autor = jsonData["resource"]["createdBy"]["displayName"]

    eventMsg = eventSwitcher(logFile, eventType, jsonData)
    print(eventMsg)
    msg = "{\"text\":\"" + eventMsg + "\"}"

    callLogger(logFile, "Iniciando envio")

    for url in range(len(webhook)):
        post = postMsg(logFile, msg, webhook[url])

    return post

def trataCodePushed(logFile, data):

    print("alo push")

    autor = data["resource"]["pushedBy"]["displayName"]
    repo = data["resource"]["repository"]["name"]
    branch = data["resource"]["repository"]["defaultBranch"]
    markdownMsg = data["detailedMessage"]["markdown"]

    branch = branch.split("/")

    commits = markdownMsg.split("\r\n* ")

    print(commits)

    eventLine = "\\nMerge realizado no repositório " + repo + ", branch " + branch[-1] + ", atualizem seus repositórios locais.\\n"

    commitList = []
    commitIdList = []
    commitUrlList = []
    commitTxt = ''
    i = 0
    for commit in data["resource"]["commits"]:
        commitList.append(commit["comment"])
        commitIdList.append(commit["commitId"])
        commitUrlList.append(commit['url'])
        commitLine = '<' + \
            str(commitUrlList[i])+'|'+str(commitIdList[i]) + \
            '> - '+str(commitList[i])
        commitTxt += (commitLine
                      if commitTxt == '\n'
                      else '\n' + commitLine)
        i += 1

    msgTxt = str("<users/all>\n"
                 + eventLine
                 + "Autor do merge: "
                 + autor
                 + "\\n\\nCommits inclusos: "
                 + commitTxt)

    return msgTxt;

def trataPullRequest(logFile, data):

    print("alo pull")

    autor = data["resource"]["createdBy"]["displayName"]
    repo = data["resource"]["repository"]["name"]
    #branch = data["resource"]["repository"]["defaultBranch"]
    urlPullRequest = data["resource"]["_links"]["web"]["href"]

    #branch = branch.split("/")

    #eventLine = "\\Merge request criado para o repositório " + repo + ", branch " + branch[-1] + ", necessário Code Review.\\n"
    eventLine = "\\Merge request criado para o repositório " + repo + ", necessário Code Review.\\n"

    msgTxt = str("<users/all>\n"
                 + eventLine
                 + "Criado por: "
                 + autor
                 + "\\nLink para Code Review: "
                 + urlPullRequest)

    return msgTxt;
