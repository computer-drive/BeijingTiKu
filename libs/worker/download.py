from PyQt5.QtCore import QThread, pyqtSignal, Qt
from qfluentwidgets import InfoBar
from libs.consts import *
import requests
import time
import logging
class Downloader(QThread):
    finished = pyqtSignal(tuple)
    update = pyqtSignal(tuple)

    def __init__(self, url: str, save_path: str, headers=HEADERS):
        self.url = url
        self.save_path = save_path
        self.headers = headers

        super().__init__()

    def run(self):
        
        try:
            # print(self.url, self.headers)
            response = requests.get(self.url, headers=self.headers, stream=True)

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
        except KeyboardInterrupt as e:
            self.finished.emit((False, e))


        # print(self.progress.value())
print(f"    -<Function> download_file")
def download_file(url:str, save_path:str, title:str, headers=HEADERS, parent=None):
    from ..pages.progress_window import ProgressWindow

    logger = logging.getLogger("Main")

    def finish(data):

        progress_window.close()
        if data[0]:
            InfoBar.success(
                "下载成功",
                f"文件已保存到: {save_path}",
                orient=Qt.Vertical,
                parent=parent,
                duration=INFO_BAR_DURATION
            )
            logger.info(f"Download successful.", extra={"class": "Downloader"})
        else:
            InfoBar.error(
                "下载失败",
                f"详细信息请查看日志文件",
                orient=Qt.Vertical,
                parent=parent,
                duration=INFO_BAR_DURATION
            )
            logger.error(f"Download failed. details: {data[1]}", extra={"class": "Downloader"})


    
    logger.info(f"Starting download:{url}", extra={"class": "Downloader"})
    progress_window = ProgressWindow(title, parent)

    progress_window.worker = Downloader(url, save_path, headers)
    progress_window.worker.update.connect(progress_window.update_)   
    progress_window.worker.finished.connect(finish)

    progress_window.worker.start()

    progress_window.show()