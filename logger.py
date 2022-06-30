from datetime import datetime
import os


def logger(logFile, msg):
    with open(logFile, mode="a", encoding='utf-8') as appendLog:
        timestamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S - ")
        logLine = (timestamp
                   + msg
                   + '\n')
        appendLog.write(logLine)


def callLogger(logFile, msg):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    logPath = ROOT_DIR + '\\logging\\'

    fullLogFile = logPath + logFile

    if(not os.path.exists(logPath)):
        os.makedirs(logPath)

    print(msg)
    logger(fullLogFile, msg)
