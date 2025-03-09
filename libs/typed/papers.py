import typing
from . import ResultDict

class PaperDict(typing.TypedDict):
    id: int
    store_name: str
    cate_id: str
    image: str
    sales: str
    price: str
    stock: int
    upload_people: str
    upload_userid: int
    add_time: str
    upload_num : int
    share_num :int
    pdf_paper: str
    pdf_answer : str
    word_paper : str
    word_answer : str
    store_type: str
    is_quality: int
    is_hot : int
    is_vipfree: int
    store_subject: str
    file_num: int
    is_official: int
    is_luckmoney: int
    all_type: str
    intersection: str
    is_blue_buy: int
    have_answer: str
    order_z: int
    order_s: int
    district: str
    if_download: int
    svip_free: bool
    is_pay: int
    if_collect: int
    if_gocat: int
    activate: any
    pointinfo: list
    is_have_video: int
    is_have_audio: int
    count: int
    productid_str: str

class PaperResultDict(ResultDict):
    data: list[PaperDict]





