import requests
from typing import Literal
from libs.consts import *

def get_data(url, args=None, headers=HEADERS, timeout=DEFAULT_TIMEOUT, data_type:Literal["json", "text", "bytes", "response"]="json"):
    
    try:
        response = requests.get(url, params=args, headers=headers, timeout=timeout)
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


def post_data(url, data=None, headers=HEADERS, timeout=DEFAULT_TIMEOUT, data_type:Literal["json", "text", "bytes", "response"]="json"):


    try:
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
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

    status, data = get_data(SEARCH_PAPER_URL, args, timeout=DEFAULT_TIMEOUT)
    if status:
        return data["data"][0]["count"]
    else:
        return 0
