# App Info
VERSION = "1.0.69"
APP_NAME = "BeijingTiKu"

# Logger Info
LOGGER_NAME = "Main"
LOGGER_FORMAT = "%(color)s[%(asctime)s][%(class_name)s/%(levelname)s]%(extra_name)s%(message)s"

# Path Info
CONFIG_PATH = "config.json"
AVATOR_PATH = "avator.jpg"
REPORT_PATH = "logs/report/"
FILE_PATH = "data\\files\\"
LOG_PATH = "logs"
ICON_PATH = "resources/icons/"

# Icon Path Info
ICON_PATHS = {
    "pdf": f"{ICON_PATH}pdf.png",
    "word": f"{ICON_PATH}word.png",
}

DEPEND_PATH = [
    "data",
    "data/files",
    "logs",
    "logs/report",
]

# Config File Info
CONFIG_ACCOUNT_LOGIN = "account.login"
CONFIG_ACCOUNT_NAME = "account.name"
CONFIG_ACCOUNT_TOKEN = "account.token"
CONFIG_ACCOUNT_IS_VIP = "account.is_vip"
CONFIG_ACCOUNT_PHONE = "account.phone"
CONFIG_COLLECTS = "collects"


# Widget Info
PROGRESS_RING_SIZE = (45, 45)
INFO_BAR_DURATION = 5000

# Style Info
SCROLL_AERA_STYLE = "QScrollArea{background: transparent; border: none}"
SCROLL_WIDGET_STYLE = "QWidget{background: transparent;}"

# Search Page Info
SEARCH_STATE = ["小学", "初中", "高中"]
SEARCH_SUBJECT = [
    "语文",
    "数学",
    "英语",
    "物理",
    "化学",
    "生物",
    "历史",
    "地理",
    "政治",
]
SEARCH_PREFERRED_TYPE = ["全部", "汇编", "测试", "课件", "讲义", "知识", "专辑"]
SEARCH_PAPER_TYPE = [
    "全部",
    "真题",
    "(上)期中",
    "(上)期末",
    "(下)期中",
    "(下)期末",
    "一模",
    "二模",
    "月考",
    "合格考试",
    "分班考试",
    "真题汇编",
    "(上)期中汇编",
    "(上)期末汇编",
    "(下)期中汇编",
    "(下)期末汇编",
    "一模汇编",
    "二模汇编",
    "合格考汇编",
]
SEARCH_REGION = [
    "北京",
    "海淀",
    "西城",
    "朝阳",
    "东城",
    "房山",
    "石景山",
    "顺义",
    "昌平",
    "通州",
    "大兴",
    "门头沟",
    "延庆",
    "怀柔",
    "密云",
    "经开",
    "燕山",
    "延庆",
]
SEARCH_ASSEMBLE_TYPE = [
    "全部",
    "(上)期末汇编",
    "(上)其中汇编",
    "一模汇编",
    "二模汇编",
    "(下)期中汇编",
    "(下)期末汇编",
    "合格考汇编",
]

PRIMARY_GRADE = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]
MIDDLE_GRADE = ["初一", "初二", "初三"]
HIGH_GRADE = ["高一", "高二", "高三"]

SEARCH_NULL_TEXT = "(>_<)"

PAPERS_DEFAULT_LIMIT = 20
PREFERRED_DEFAULT_LIMIT = 10

# Local Page Info
TAB_TEXT = ["收藏", "下载", "历史"]

# Urls
DOWNLOAD_URL = "https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com"
WEB_URL = "https://www.jingshibang.com/home/detailPaper/"
SEARCH_PAPER_URL = "https://www.jingshibang.com/api/products"
SEARCH_PREFERRED_URL = "https://www.jingshibang.com/api/smallclass/paperlist"
CATEGORY_URL = "https://www.jingshibang.com/api/smallclass/getcategory"
LOGIN_GET_PIC_URL = "https://www.jingshibang.com/api/getwxpic"
LOGIN_URL = "https://www.jingshibang.com/api/wechat/pcauth2"
GET_PREFERRED_URL = "https://www.jingshibang.com/api/product/detail/"


# Requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

HEADERS = {"User-Agent": USER_AGENT}

DEFAULT_TIMEOUT = 10

# Others
WINDOW_TITLE = APP_NAME

ERROR_TEXT = "(⊙x⊙;)"
