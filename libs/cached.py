import json

def cachePapersInfo(papers:list[dict]):
    with open("data/papers.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    with open("data/papers.json", "w", encoding="utf-8") as f:
        data["papers"].extend(papers)
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    

def cachePreferredInfo(preferred:list[dict]):
    with open("data/preferred.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    with open("data/preferred.json", "w", encoding="utf-8") as f:
        data["preferred"].extend(preferred)
        f.write(json.dumps(data, ensure_ascii=False, indent=4))   


    
