from post import postMsg
from logger import callLogger
import json


def prepareMsg(logFile, data, webhook):

    data = data.replace("'", '"')
    jsonData = json.loads(data)

    autor = jsonData["resource"]["pushedBy"]["displayName"]
    repo = jsonData["resource"]["repository"]["name"]
    branch = jsonData["resource"]["repository"]["defaultBranch"]

    commitList = []
    commitIdList = []
    commitUrlList = []
    commitTxt = ''
    i = 0
    for commit in jsonData["resource"]["commits"]:
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

    branch = branch.split("/")

    msgTxt = str("<users/all>\n"
                 + "\\nMerge realizado no repositório "
                 + repo
                 + ", branch "
                 + branch[-1]
                 + ", atualizem seus repositórios locais.\\n"
                 + "Autor do merge: "
                 + autor
                 + "\\n\\nCommits inclusos: "
                 + commitTxt)

    msg = "{\"text\":\"" + msgTxt + "\"}"

    callLogger(logFile, "Iniciando envio")

    for url in range(len(webhook)):
        post = postMsg(logFile, msg, webhook[url])

    return post
