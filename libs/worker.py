import time 
import logging
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from qfluentwidgets import InfoBar
import requests
from typing import Literal
import time


download_count = 0

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def get_data(url, args=None, user_agent=USER_AGENT, timeout=10, data_type:Literal["json", "text", "bytes", "response"]="json"):
    headers = {
        "User-Agent": user_agent
    }
    
    try:
        response = requests.get(url, params=args, headers=headers, timeout=timeout)
        # print(response.url)
        if response.ok:
            match data_type:
                case "json":
                    return (True, response.json())
                case "text":
                    return (True, response.text)
                case "bytes":
                    return (True, response.content)
                case "response":
                    return (True, response)
        else:
            return (False, response.status_code)

    except Exception as e:
        return (False, e)
    
def post_data(url, data=None, user_agent=USER_AGENT, timeout=10, data_type:Literal["json", "text", "bytes", "response"]="json"):
    headers = {
        "User-Agent": user_agent
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
        # print(response.url)
        if response.ok:
            match data_type:
                case "json":
                    return (True, response.json())
                case "text":
                    return (True, response.text)
                case "bytes":
                    return (True, response.content)
                case "response":
                    return (True, response)
        else:
            return (False, response.status_code)

    except Exception as e:
        return (False, e)
    
def get_total(args):
    args["page"] = 114514

    status, data = get_data("https://www.jingshibang.com/api/products", args, timeout=10)
    if status:
        return data["data"][0]["count"]
    else:
        return 0

class RequestsWorker(QThread):
    finished = pyqtSignal(tuple)

    def __init__(self, url, args=None, user_agent=USER_AGENT, timeout=10):
        super().__init__()

        self.url = url
        self.args = args
        self.user_agent = user_agent
        self.timeout = timeout

    def __run__(self):
        status, data = get_data(self.url, self.args, self.user_agent, self.timeout)

        return (status, data)


class SearchWorker(RequestsWorker):
    def __init__(self, keyword, subject, grade, type, time, place, page, limit=20, get_total=False):
        self.args = {
            "page": page,
            "limit": limit,
            "keyword": keyword,
            "store_subject": subject,
            "store_grade": grade,
            "store_type": type,
            "store_year": time,
            "district": place,
        }

        super().__init__(
            "https://www.jingshibang.com/api/products",
            self.args
        )

    def run(self):
        status, data = self.__run__()

        if status:
            total = get_total(self.args)
            self.finished.emit((status, data["data"], total))
        else:
            self.finished.emit((status, data["data"], 0))

class Downloader(QThread):
    finished = pyqtSignal(tuple)
    update = pyqtSignal(tuple)

    def __init__(self, url: str, save_path: str, user_agent: str = USER_AGENT):
        self.url = url
        self.save_path = save_path
        self.user_agent = user_agent

        super().__init__()

    def run(self):
        headers = {
            "User-Agent": self.user_agent
        }
        
        try:
            response = requests.get(self.url, headers=headers, stream=True)

            count = 0
            total = int(response.headers.get("Content-Length", 1))
            start_time = time.perf_counter()
            chunk_size = int(total / 100)

            with open(self.save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        # print(threading.current_thread().name)
                        time.sleep(0)
                        count += len(chunk)

                        speed = count / (time.perf_counter() - start_time)
                        if speed > 0:
                            eta = (total - count) / speed
                        else:
                            eta = -1
                        progress = int(count / total * 100.0)

                        self.update.emit((count, total, speed, eta, progress))
                        
                        f.write(chunk)

            self.finished.emit((True, None))
        except Exception as e:
            self.finished.emit((False, e))


        # print(self.progress.value())

def download_file(url:str, save_path:str, title:str, user_agent:str=USER_AGENT, parent=None):
    from libs.pages import ProgressWindow

    logger = logging.getLogger("Main")

    def finish(data):

        progress_window.close()
        if data[0]:
            InfoBar.success(
                "下载成功",
                f"文件已保存到: {save_path}",
                orient=Qt.Vertical,
                parent=parent,
                duration=5000
            )
            logger.info(f"Download successful.", extra={"class": "Downloader"})
        else:
            InfoBar.error(
                "下载失败",
                f"详细信息请查看日志文件",
                orient=Qt.Vertical,
                parent=parent,
                duration=5000
            )
            logger.error(f"Download failed. details: {data[1]}", extra={"class": "Downloader"})


    
    logger.info(f"Starting download:{url}", extra={"class": "Downloader"})
    progress_window = ProgressWindow(title, parent)

    progress_window.worker = Downloader(url, save_path, user_agent)
    progress_window.worker.update.connect(progress_window.update_)   
    progress_window.worker.finished.connect(finish)

    progress_window.worker.start()

    progress_window.show()


class GetCategoryWorker(RequestsWorker):

    def __init__(self):
        super().__init__("https://www.jingshibang.com/api/smallclass/smallclasscategory")
    
    def run(self):
        status, data = self.__run__()

        if status:
            self.finished.emit((True, data))
        else:
            self.finished.emit((False, data))

class GetPointsWorker(RequestsWorker):
    
    def __init__(self, pid):
        args = {
            "pid": pid,
            "level": 2
        }
        super().__init__(f"https://www.jingshibang.com/api/smallclass/getcategory", args)
        self.pid = pid


    def run(self):
        status, data = self.__run__()


        self.finished.emit((status, data, self.pid))

class GetPapersListWorker(RequestsWorker):

    def __init__(self, page, subject, grade, limit=10):
        super().__init__(f"https://www.jingshibang.com/api/smallclass/paperlist")

        self.args = {
            "is_pc": 1,
            "page": page,
            "limit": limit,
            "store_subject": subject,
            "store_grade": grade,
            "store_type": "",
            "store_year": None,
            "moudle": None,
            "chapter": None,
            "pointid": None,
            "moudle_name": "",
            "chapter_name": "",
            "point_name": "",
            "assembly_grade": "",
            "assembly_type": "",
            "catid": "",
            "type": 0
        }

    def setType(self, type):
        self.args["store_type"] = type
        return self

    def setYear(self, year):
        self.args["store_year"] = year
        return self
    
    def setModule(self, id, name):
        self.args["moudle"] = id
        self.args["moudle_name"] = name
        return self

    def setChapter(self, id, name):
        self.args["chapter"] = id
        self.args["chapter_name"] = name
        return self
    
    def setPoint(self, id, name):
        self.args["pointid"] = id
        self.args["point_name"] = name
        return self

    def setAssembly(self, grade, type):
        self.args["assembly_grade"] = grade
        self.args["assembly_type"] = type
        return self

    def setCatid(self, moudle, chapter, point):
        
        if point is not None:
            self.args["catid"] = point
        elif chapter is not None:
            self.args["catid"] = chapter
        else:
            self.args["catid"] = moudle
        # print(self.args["catid"])

        return self

    def build(self):
        return self.args
    

    
    def run(self):
        status, data = self.__run__()
        
        self.finished.emit((status, data))

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
        status, wxpic = post_data("https://www.jingshibang.com/api/getwxpic", {})
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

            status, data = get_data("https://www.jingshibang.com/api/wechat/pcauth2", {"wechat_flag": flag})

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


