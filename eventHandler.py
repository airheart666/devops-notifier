from utils import findCommits, findDefaultBranch


def eventSwitcher(eventType, data):
    '''
    Função faz as chamadas de funções específicas para cada evento, através de um dict, com base no tipo de evento recebido
    '''
    switcher = {
            "git.pullrequest.updated.completed": trataPullCompleted,
            "git.pullrequest.created": trataPullCreated
        }
    msg = switcher[eventType](data)
    return msg


def trataPullCreated(data):

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


def trataPullCompleted(data):

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
