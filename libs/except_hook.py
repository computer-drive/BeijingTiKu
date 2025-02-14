from datetime import datetime
from traceback import format_tb
from os.path import exists
from os import makedirs
from logging import getLogger
from json import dumps
from sys import exit, argv



def except_hook(exctype, value, tb):
    logger = getLogger("Main")


    tb_str =  ''.join(format_tb(tb))

    logger.error(f"Uncaught exception while running: {exctype.__name__}: {value} ")
    logger.error(f"Traceback:\n {tb_str}\n   {exctype.__name__}: {value}")

    if not exists("logs/report/"):
        makedirs("logs/report/")
    
    now = datetime.now()

    with open(f"logs/report/{now.strftime('%Y-%m-%d %H-%M')}.json", "w", encoding="utf-8") as f:
        f.write(dumps({
            "app": "BeijingTiKu",
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "error_type": f"{exctype.__name__}:{value}",
            "traceback": f"{tb_str}\n   {exctype.__name__}: {value}",
            "app_path": argv[0]
        },
        indent=4, ensure_ascii=False))

    exit(1)