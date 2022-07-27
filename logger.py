from datetime import datetime
import os


def logger(logFile, logLine):
    with open(logFile, mode="a", encoding='utf-8') as appendLog:
        timestamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S - ")
        fullLogLine = (timestamp
                       + logLine
                       + '\n')
        appendLog.write(fullLogLine)


def callLogger(logLine):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    logPath = ROOT_DIR + '/logging/'

    timestamp = (datetime.now()).strftime("%Y-%m-%d")

    fullLogFile = logPath + 'devops_notifier' + timestamp + '.log'

    if(not os.path.exists(logPath)):
        os.makedirs(logPath)

    print(logLine)
    logger(fullLogFile, logLine)
