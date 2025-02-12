import time 
import logging
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from qfluentwidgets import InfoBar
import requests


download_count = 0

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def get_total(args):
    args["page"] = 114514

    try:
        r = requests.get("https://www.jingshibang.com/api/products", params=args)

        return r.json()["data"][0]["count"]
    
    except Exception as e:
        return 0



class SearchWorker(QThread):
    finished = pyqtSignal(tuple)

    def __init__(self, keyword, subject, grade, type, time, place, page, limit=20, get_total=False):
        super().__init__()

        self.keyword = keyword
        self.subject = subject
        self.grade = grade
        self.type = type
        self.time = time
        self.place = place
        self.page = page
        self.limit = limit
    
    def run(self):
        args = {
            "page": self.page,
            "limit": self.limit,
            "keyword": self.keyword,
            "store_subject": self.subject,
            "store_grade": self.grade,
            "store_type": self.type,
            "store_year": self.time,
            "district": self.place,
        }

        headers = {
            "User-Agent": USER_AGENT
        }

        try:
            response = requests.get("https://www.jingshibang.com/api/products",
                                    headers=headers, params=args)
            
            if response.ok:

                data = response.json()

                if get_total:
                    total = get_total(args)
                    self.finished.emit((True, data["data"], total))
                else:
                    self.finished.emit((True, data["data"], 0))
            else:
                self.finished.emit((False, response.status_code))
        
        except Exception as e:
            self.finished.emit((False, e))

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
    logger = logging.getLogger("__main__")

    def finish(data):
        global download_count
        # print(parent)
        progress_window.close()
        if data[0]:
            InfoBar.success(
                "下载成功",
                f"文件已保存到: {save_path}",
                orient=Qt.Vertical,
                parent=parent,
                duration=5000
            )
            logger.info(f"Download successful.", extra={"type_name": f"downloader-{download_count}"})
        else:
            InfoBar.error(
                "下载失败",
                f"详细信息请查看日志文件",
                orient=Qt.Vertical,
                parent=parent,
                duration=5000
            )
            logger.error(f"Download failed. details: {data[1]}", extra={"type_name": f"downloader-{download_count}"})

        download_count += 1

    
    logger.info(f"Starting download:{url}", extra={"type_name": f"downloader-{download_count}"})
    progress_window = ProgressWindow(title, parent)

    progress_window.worker = Downloader(url, save_path, user_agent)
    progress_window.worker.update.connect(progress_window.update_)   
    progress_window.worker.finished.connect(finish)

    progress_window.worker.start()

    progress_window.show()

class GetCategoryWorker(QThread):
    finished = pyqtSignal(tuple)
    
    def __init__(self, user_agent:str=USER_AGENT):
        super().__init__()
        self.user_agent = user_agent

    def run(self):
        headers = {
            "User-Agent": self.user_agent
        }
        try:
            response = requests.get("https://www.jingshibang.com/api/smallclass/smallclasscategory", headers=headers)
            if response.ok:
                self.finished.emit((True, response.json()))
            else:
                self.finished.emit((False, response.status_code))
        except Exception as e:
            self.finished.emit((False, e))





# if __name__ == "__main__":
    # app = QApplication([])


    # w = FluentWindow()


    # loading.show()



    # w.show()

    # app.exec_()
