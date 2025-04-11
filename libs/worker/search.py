from .request_worker import RequestsWorker
from libs.consts import *
from .request import get_data
# from ..typed.papers import PaperDict


def get_total(args):
    args["page"] = 114514

    status, data = get_data(SEARCH_PAPER_URL, args, timeout=DEFAULT_TIMEOUT)
    if status:
        return data["data"][0]["count"]
    else:
        return 0


class SearchWorker(RequestsWorker):
    def __init__(
        self,
        keyword,
        subject,
        grade,
        type,
        time,
        place,
        page,
        limit=20,
        get_total=False,
    ):
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

        super().__init__(SEARCH_PAPER_URL, self.args)

    def run(self):
        status, data = self.__run__()

        if status:
            total = get_total(self.args)

            self.finished.emit((status, data["data"], total))
        else:
            self.finished.emit((status, data["data"], 0))
