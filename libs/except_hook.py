from datetime import datetime
from traceback import format_tb
from os.path import exists, join
from os import makedirs, getcwd
from os import _exit
from logging import getLogger
from json import dumps
from sys import argv
from libs.consts import *
from PySide6.QtCore import qInstallMessageHandler, QtMsgType
from .log import logger

def qt_message_handler(type, context, message):

    content = f"{message}"

    match type:
        case QtMsgType.QtDebugMsg:
            logger.debug(content, "Qt")
        case QtMsgType.QtWarningMsg:
            logger.warning(content, "Qt", "test")
        case QtMsgType.QtCriticalMsg:
            logger.error(content, "Qt")
        case QtMsgType.QtFatalMsg:
            logger.error(content, "Qt")
        case QtMsgType.QtInfoMsg:
            logger.info(content, "Qt")
        case QtMsgType.QtSystemMsg:
            logger.info(content, "Qt")

qInstallMessageHandler(qt_message_handler)


def except_hook(exctype, value, tb):
    tb_str = "".join(format_tb(tb))

    logger.error(f"Uncaught exception while running: {exctype.__name__}: {value} ")
    logger.error(f"Traceback:\n {tb_str}\n   {exctype.__name__}: {value}")

    if not exists(REPORT_PATH):
        makedirs(REPORT_PATH)

    now = datetime.now()

    with open(
        f"{REPORT_PATH}/{now.strftime('%Y-%m-%d %H-%M')}.json", "w", encoding="utf-8"
    ) as f:
        f.write(
            dumps(
                {
                    "app": APP_NAME,
                    "time": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "error_type": f"{exctype.__name__}:{value}",
                    "traceback": f"{tb_str}\n   {exctype.__name__}: {value}",
                    "app_path": argv[0],
                    "log": join(getcwd(), "logs", f"{now.strftime('%Y-%m-%d')}.log"),
                },
                indent=4,
                ensure_ascii=False,
            )
        )

    _exit(1)



