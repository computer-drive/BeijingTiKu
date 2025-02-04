import logging
import colorlog
import os
import threading
from utility.ansi import fore, back, style

class LogFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        record.type_name = getattr(record, 'type_name', 'main')

        record.thread = threading.current_thread().name
        record.levelname = record.levelname.lower()
        record.color = ""
        

        match record.levelname:
            case 'debug':
                record.color = fore.CYAN
            case 'info':
                record.levelname = f"{fore.BLUE}{record.levelname}{style.RESET}"
            case 'warning':
                record.color = fore.YELLOW
            case 'error':
                record.color = fore.RED
            case 'critical':
                record.color = fore.RED

        
        return super().format(record)
    

def create_logger(name:str = "",
                  level:int = logging.INFO,
                  format:str = "%(color)s%(type_name)s %(levelname)s %(message)s%(reset)s",
                  file_logger:bool = True,
                  file_logger_path:str = "logs",
                  file_logger_name:str = "app.log"
                  ):
    logger = colorlog.getLogger(name)
    logger.setLevel(level)

    formatter = LogFormatter(
        format,
        reset=True
    )
    
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    if file_logger:
        if not os.path.exists(file_logger_path):
            os.mkdir(file_logger_path)
        file_handler = logging.FileHandler(f"{file_logger_path}/{file_logger_name}")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

    return logger


