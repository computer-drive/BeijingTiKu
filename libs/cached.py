import json
import os



def initCacheFile():
    if not os.path.exists("data/papers.json"):
        with open("data/papers.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({"papers": []}, ensure_ascii=False))
    
    if not os.path.exists("data/preferred.json"):
        with open("data/preferred.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({"preferred": []}, ensure_ascii=False))
        

def cachePapersInfo(papers:list[dict]):
    with open("data/papers.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    for paper in papers:
        if paper in data["papers"]:
            continue
        data["papers"].append(paper)

    with open("data/papers.json", "w", encoding="utf-8") as f:
        
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    

def cachePreferredInfo(preferred:list[dict]):
    with open("data/preferred.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    for item in preferred:
        if item in data["preferred"]:
            continue
        data["preferred"].append(item)

    with open("data/preferred.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))   



