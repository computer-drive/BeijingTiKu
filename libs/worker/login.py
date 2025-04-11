from PySide6.QtCore import QThread, Signal
from .request import post_data, get_data
from libs.consts import *
import time

from ..log import logger


class LoginWorker(QThread):
    got_qrcode = Signal(bytes)
    logined = Signal(tuple)
    error = Signal(tuple)
    got_avator = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__stop__ = False

    def stop(self):
        self.__stop__ = True

    def run(self):
        status, wxpic = post_data(LOGIN_GET_PIC_URL, {})
        if status:
            if wxpic["status"] == 200:
                qrcode_url = wxpic["data"]["url"]
                flag = wxpic["data"]["weChatFlag"]

                logger.info(f"Got LoginQrcodeUrl:{wxpic['data']['url']}")
                logger.info(f"Got LoginWechatFlag:{wxpic['data']['weChatFlag']}")
            else:
                logger.error(f"Get LoginQrcodeUrl Error:{wxpic['msg']}")
                self.error.emit(("getQrcode", wxpic["msg"]))
                return
        else:
            logger.error(f"Get LoginQrcodeUrl Error:{wxpic}")
            self.error.emit(("getQrcode", wxpic))
            return

        status, qrcode = get_data(qrcode_url, data_type="bytes")

        if status:
            logger.info(f"Got LoginQrcode.")
            self.got_qrcode.emit(qrcode)
        else:
            logger.info(f"Get LoginQrcode Error:{qrcode}")
            self.error.emit(("getQrcode", qrcode))
            return

        logined = False
        token = ""
        username = ""
        phone = ""
        is_vip = False
        avator_url = ""

        while True:
            if self.__stop__:
                logger.info("Stopped.")
                return

            status, data = get_data(LOGIN_URL, {"wechat_flag": flag})

            if status:
                if data["status"] == 200:

                    logined = True
                    token = data["data"]["token"]
                    username = data["data"]["wechatInfo"]["nickname"]
                    phone = data["data"]["wechatInfo"]["phone"]
                    if data["data"]["wechatInfo"]["is_vip"] == 1:
                        is_vip = True

                    avator_url = data["data"]["wechatInfo"]["avatar"]

                    logger.info("Login success.")
                    logger.info(f"Token:{token}")
                    logger.info(f"Username:{username} Phone:{phone}  IsVip:{is_vip} ")
                    break

                else:
                    logger.info(f"Wait logining...")

            else:
                logger.error(f"Login failed:{data}")
                self.error.emit(("login", data))
                return

            time.sleep(1)

        if logined:
            self.logined.emit((token, username, phone, is_vip, avator_url))
        else:

            self.error.emit(("login", "unknown"))
            return

        status, data = get_data(avator_url, data_type="bytes")

        if status:
            with open("data/avator.jpg", "wb") as f:
                f.write(data)

            self.got_avator.emit(True)
        else:
            self.error.emit(("avator", data))
