from .request_worker import RequestsWorker
from PySide6.QtCore import Signal
from libs.consts import *
import logging

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

    def __init__(self, page, subject, grade, limit=10, logger=None):
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

        self.logger = logger


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

        args_str = ""
        for k, v in self.args.items():
            args_str += f"          {k}: {v}\n"
        args_str = args_str[:-1]

        self.logger.info(f'''Start searching with args:
{args_str}''')

        status, data = self.__run__()

        self.logger.info(f"Search finished with data: {str(data)[:20]}...more{len(str(data)) - 20}")
        
        self.finished.emit((status, data))

class GetPreferredInfoWorker(RequestsWorker):
    finished = Signal(tuple)

    def __init__(self, id, config, logger: logging.Logger, parent=None):
        
        token = config.get(CONFIG_ACCOUNT_TOKEN, "")
        headers = {
            "Authorization": f"Bearer {token}",
            "Authori-Zation": f"Bearer {token}"
        }
        super().__init__(f"{GET_PREFERRED_URL}{id}", headers=headers)

        self.config = config
        self.logger = logger

    def run(self):
        status, data = self.__run__()
        
        if status:
            if data["status"] == 200:
                self.finished.emit((True, data["data"]))
            else:
                self.finished.emit((False, data["data"]))
        else:
            self.finished.emit((False, data))
