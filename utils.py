import requests
import base64
import json
import os


def findCommits(commitUrl, commitId):
    '''
    Função busca a lista de commits vinculados ao push,
    via request na API do Azure DevOps
    '''
    authorization = getPat()

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
    '''
    Função busca o branch padrão do repositório de destino,
    via request na API do Azure DevOps
    '''

    authorization = getPat()

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


def getPat():
    '''
    Função pega o Personal Access Token (PAT) que será usado nas requisições na API do Azure DevOps
    '''
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    patPath = ROOT_DIR + "/pat.txt"
    with open(patPath, "r") as f:
        pat = f.read().rstrip()

    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

    return authorization
