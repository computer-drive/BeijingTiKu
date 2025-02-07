import os
import json

def cache_info(data:dict):
    with open("cache/info.json", "w", encoding="utf-8") as f:
        file_data = json.loads(f.read())
    
    file_data["data"].append(data)

    with open("cache/info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(file_data, indent=4, ensure_ascii=False))

def cache_infos(data:list):
    with open("cache/info.json", "w", encoding="utf-8") as f:
        file_data = json.loads(f.read())

    file_data["data"].extend(data)

    with open("cache/info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(file_data, indent=4, ensure_ascii=False))

