import logging
import colorlog
import os
import threading
from libs.consts import *
from utility.ansi import fore, back, style

SUCCESS = 25

logging.addLevelName(SUCCESS, "SUCCESS")

class AppLogger(logging.Logger):
    

    def __init__(self, name):
        super().__init__(name)

    def setClassName(self, class_name, **kwargs):
        if class_name:
            kwargs["extra"] = {"class_name": class_name}
        return kwargs
        
    def debug(self, msg, class_name="Main", *args, **kwargs):
        kwargs = self.setClassName(class_name, **kwargs)
        super().debug(msg, *args, **kwargs)
    
    def info(self, msg, class_name="Main", *args, **kwargs):
        kwargs = self.setClassName(class_name, **kwargs)
        super().info(msg, *args, **kwargs)

    def warning(self, msg, class_name="Main", *args, **kwargs):
        kwargs = self.setClassName(class_name, **kwargs)
        super().warning(msg, *args, **kwargs)

    def error(self, msg, class_name="Main", *args, **kwargs):

        kwargs = self.setClassName(class_name, **kwargs)
        super().error(msg, *args, **kwargs)

    def critical(self, msg, class_name="Main", *args, **kwargs):
        kwargs = self.setClassName(class_name, **kwargs)
        super().critical(msg, *args, **kwargs)
    
    def success(self, msg, class_name="Main", *args, **kwargs):
        kwargs = self.setClassName(class_name, **kwargs)
        super().log(SUCCESS, msg, *args, **kwargs)


class LogFormatter(colorlog.ColoredFormatter):
    def format(self, record):

        record.thread = threading.current_thread().name
        record.color = ""

        

        match record.levelname:
            case 'DEBUG':
                record.color = fore.CYAN
            case 'INFO':
                record.levelname = f"{fore.BLUE}{record.levelname}{style.RESET}"
            case 'WARNING':
                record.color = fore.YELLOW
            case 'ERROR':
                record.color = fore.RED
            case 'CRITICAL':
                record.color = fore.RED
            case 'SUCCESS':
                record.color = fore.GREEN

        
        return super().format(record)



def create_logger(name:str = "",
                  level:int = logging.INFO,
                  format:str = LOGGER_FORMAT ,
                  file_logger:bool = True,
                  file_logger_path:str = LOG_PATH ,
                  file_logger_name:str = "app.log"
                  ):
    logger = AppLogger(name)
    logger.setLevel(level)

    formatter = LogFormatter(
        format,
        datefmt="%H:%M:%S",
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


