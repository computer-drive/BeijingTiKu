from PyQt5.QtCore import QThread, pyqtSignal
from .request import post_data, get_data
from libs.consts import *
import time

class LoginWorker(QThread):
    got_qrcode = pyqtSignal(bytes)
    logined = pyqtSignal(tuple)
    error = pyqtSignal(tuple)
    got_avator = pyqtSignal(bool)

    def __init__(self, logger, parent=None):
        super().__init__(parent)

        self.logger = logger

        self.__stop__ = False
    
    def stop(self):
        self.__stop__ = True
    
    def run(self):
        status, wxpic = post_data(LOGIN_GET_PIC_URL, {})
        if status:
            if wxpic["status"] == 200:
                qrcode_url = wxpic["data"]["url"]
                flag = wxpic["data"]["weChatFlag"]

                self.logger.info(f"Got LoginQrcodeUrl:{wxpic['data']['url']}")
                self.logger.info(f"Got LoginWechatFlag:{wxpic['data']['weChatFlag']}")
            else:
                self.logger.error(f"Get LoginQrcodeUrl Error:{wxpic['msg']}")
                self.error.emit(("getQrcode", wxpic["msg"]))
                return
        else:
            self.logger.error(f"Get LoginQrcodeUrl Error:{wxpic}")
            self.error.emit(("getQrcode", wxpic))
            return
        
        status, qrcode = get_data(qrcode_url, data_type="bytes")

        if status:
            self.logger.info(f"Got LoginQrcode.")
            self.got_qrcode.emit(qrcode)
        else:
            self.logger.info(f"Get LoginQrcode Error:{qrcode}")
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
                self.logger.info("Stopped.")
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

                    self.logger.info("Login success.")
                    self.logger.info(f"Token:{token}")
                    self.logger.info(f"Username:{username} Phone:{phone}  IsVip:{is_vip} ")
                    break
                
                else:
                    self.logger.info(f"Wait logining...")

            else:
                self.logger.error(f"Login failed:{data}")
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

print(f"    -<Class> GetPreferredInfoWorker")