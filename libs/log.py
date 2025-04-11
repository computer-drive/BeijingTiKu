import logging
import colorlog
import os
import threading
from libs.consts import *
from datetime import datetime
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
        # 仅在控制台日志中添加颜色
        if self.use_color:
            match record.levelname:
                case "DEBUG":
                    record.color = fore.CYAN
                case "INFO":
                    record.levelname = f"{fore.BLUE}{record.levelname}{style.RESET}"
                case "WARNING":
                    record.color = fore.YELLOW
                case "ERROR" | "CRITICAL":
                    record.color = fore.RED
                case "SUCCESS":
                    record.color = fore.GREEN
        return super().format(record)

    def __init__(self, format, datefmt=None, use_color=False):
        super().__init__(fmt=format, datefmt=datefmt, reset=use_color)
        self.use_color = use_color


class FileHandler(logging.FileHandler):
    def __init__(
        self, filename, mode="a", encoding=None, delay=False, file_format=LOGGER_FORMAT
    ):
        super().__init__(filename, mode, encoding, delay)

        self.setFormatter(
            LogFormatter(file_format, datefmt="%H:%M:%S", use_color=False)
        )

    def emit(self, record):
        try:
            msg = self.format(record)

            stream = self.stream

            stream.write(msg + self.terminator)

            self.flush()

        except Exception:
            self.handleError(record)


def create_logger(
    name: str = "",
    level: int = logging.INFO,
    console_format: str = LOGGER_FORMAT,  # 含颜色字段的格式
    file_logger: bool = True,
    file_logger_path: str = LOG_PATH,
    file_logger_name: str = "app.log",
    file_format: str = LOGGER_FORMAT,  # 无颜色字段的格式
):
    logger = AppLogger(name)
    logger.setLevel(level)

    # 文件处理器使用普通格式器
    if file_logger:
        os.makedirs(file_logger_path, exist_ok=True)

        file_handler = FileHandler(f"{file_logger_path}/{file_logger_name}")
        logger.addHandler(file_handler)

    # 控制台处理器使用带颜色的格式器
    console_handler = colorlog.StreamHandler()
    console_formatter = LogFormatter(console_format, datefmt="%H:%M:%S", use_color=True)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


now = datetime.now()  # 获取当前时间
logger = create_logger(
    LOGGER_NAME, file_logger_name=f"{now.strftime('%Y-%m-%d')}.log"  # 创建日志记录器
)  # 设置日志文件名
