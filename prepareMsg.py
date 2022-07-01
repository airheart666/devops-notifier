from post import postMsg
from logger import callLogger
import json
import requests
import base64


def eventSwitcher(logFile, eventType, data):

    switcher = {
            "git.pullrequest.updated": trataPullCompleted,
            "git.pullrequest.created": trataPullRequest
        }
    msg = switcher[eventType](logFile, data)
    return msg


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


def trataPullCompleted(logFile, data):

    print("alo push")

    autor = data["resource"]["createdBy"]["displayName"]
    repo = data["resource"]["repository"]["name"]
    repoUrl = data["resource"]["repository"]["url"]
    sourceCommitUrl = data["resource"]["lastMergeSourceCommit"]["url"]
    sourceCommitId = data["resource"]["lastMergeSourceCommit"]["commitId"]

    branch = findDefaultBranch(repoUrl)

    eventLine = "\\nMerge realizado no repositório " + repo + ", branch " + \
        branch[-1] + ", atualizem seus repositórios locais.\\n"

    commitMsg = findCommits(sourceCommitUrl, sourceCommitId)

    msgTxt = str("<users/all>\n"
                 + eventLine
                 + "Autor do merge: "
                 + autor
                 + "\\n\\nCommits inclusos: "
                 + commitMsg)

    return msgTxt


def trataPullRequest(logFile, data):

    print("alo pull")

    autor = data["resource"]["createdBy"]["displayName"]
    repo = data["resource"]["repository"]["name"]
    urlPullRequest = data["resource"]["_links"]["web"]["href"]
    sourceCommitUrl = data["resource"]["lastMergeSourceCommit"]["url"]
    sourceCommitId = data["resource"]["lastMergeSourceCommit"]["commitId"]

    commitMsg = findCommits(sourceCommitUrl, sourceCommitId)

    eventLine = "\\Merge request criado para o repositório " + \
        repo + ", necessário Code Review.\\n"

    msgTxt = str("<users/all>\n"
                 + eventLine
                 + "Criado por: "
                 + autor
                 + "\\nLink para Code Review: "
                 + urlPullRequest
                 + "\\n\\nCommits inclusos: "
                 + commitMsg)

    return msgTxt


def findCommits(commitUrl, commitId):

    pat = '4iulu6qlgw4lyiddq2hxpr4kg4mz4jeevxsf45exu4b2x2ydlhmq'
    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+authorization
    }

    commit = requests.get(
        url=commitUrl,
        headers=headers
    )

    commitData = json.loads(commit.text)

    pushId = commitData["push"]["pushId"]

    url = commitUrl.replace('/' + str(commitId), '')

    pushUrl = url + "?pushId=" + str(pushId)

    push = requests.get(
        url=pushUrl,
        headers=headers
    )

    pushData = json.loads(push.text)

    commitList = pushData["value"]

    commitCommentList = []
    commitIdList = []
    commitUrlList = []
    commitTxt = ''
    i = 0
    for commit in commitList:

        commitJson = json.loads(str(json.dumps(commitList[i])))

        commitCommentList.append(commitJson["comment"])
        commitIdList.append(commitJson["commitId"])
        commitUrlList.append(commitJson["remoteUrl"])
        commitLine = '<' + \
            str(commitUrlList[i])+'|'+str(commitIdList[i]) + \
            '> - '+str(commitCommentList[i])
        commitTxt += (commitLine
                      if commitTxt == '\n'
                      else '\n' + commitLine)
        i += 1

    return commitTxt


def findDefaultBranch(repoUrl):

    pat = '4iulu6qlgw4lyiddq2hxpr4kg4mz4jeevxsf45exu4b2x2ydlhmq'
    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+authorization
    }

    repo = requests.get(
        url=repoUrl,
        headers=headers
    )

    repoData = json.loads(repo.text)
    branchPath = repoData["defaultBranch"]
    branch = branchPath.split("/")

    return branch
