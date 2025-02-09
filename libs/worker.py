from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication
from qfluentwidgets import FluentWindow, MessageBoxBase, TitleLabel, ProgressBar, CaptionLabel, PushButton, InfoBar
import requests
import time
import threading 
from utility.format import *
import logging

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

class ProgressWindow(MessageBoxBase):
    def __init__(self, content: str, parent=None):
        super().__init__(parent)


        self.viewLayout.addWidget(TitleLabel(content))

        self.progress = ProgressBar()
        self.progress.setRange(0, 100)
        self.viewLayout.addWidget(self.progress)

        info_layout = QHBoxLayout()
        self.viewLayout.addLayout(info_layout)

        self.count_label = CaptionLabel("0.00 MB / 0.00 MB 0.00 KB/S")
        info_layout.addWidget(self.count_label)

        self.eta_label = CaptionLabel("00:00:00 100%")
        info_layout.addWidget(self.eta_label, alignment=Qt.AlignmentFlag.AlignRight)

        self.widget.setMinimumWidth(450)

        self.yesButton.hide()
        # self.cancelButton.hide()

    def update_(self, data):
        count, total, speed, eta, progress = data

        

        if eta == -1:
            eta = "--:--:--"
        

        self.count_label.setText(f"{format_capacity(count)} / {format_capacity(total)} {format_capacity(speed)}/S")
        self.eta_label.setText(f"{format_time(eta)} {progress}%") 

        self.progress.setValue(progress)
        # print(self.progress.value())

def download_file(url:str, save_path:str, title:str, user_agent:str=USER_AGENT, parent=None):
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

if __name__ == "__main__":
    app = QApplication([])

    def clicked():
        def finish(data):
            progress_window.close()
            if data[0]:
                print("下载成功")
            else:
                print("下载失败", data[1])

    

        progress_window = ProgressWindow("Downloading", w)

        progress_window.worker = Downloader("https://www.jingshibang.com/uploads/paper/file/1736663337/2025%E5%8C%97%E4%BA%AC%E6%B5%B7%E6%B7%80%E5%88%9D%E4%BA%8C%EF%BC%88%E4%B8%8A%EF%BC%89%E6%9C%9F%E6%9C%AB%E8%8B%B1%E8%AF%AD%EF%BC%88%E6%95%99%E5%B8%88%E7%89%88%EF%BC%89.pdf", "1.pdf")
        progress_window.worker.update.connect(progress_window.update)
        progress_window.worker.finished.connect(finish)

        progress_window.worker.start()
        progress_window.show()

    w = FluentWindow()

    button = PushButton("Download")
    w.layout().addWidget(button)

    button.clicked.connect(clicked)

    w.show()

    app.exec_()
