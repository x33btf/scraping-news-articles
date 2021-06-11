def newEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "site" : item["site"],
        "title" : item["title"],
        "author" : item["author"],
        "desc" : item["desc"],
        "content" : item["content"],
        "date" : item["date"],
        "img" : item["img"],
        "category" : item["category"]
    }

def newsEntity(items) -> list:
    return [ newEntity(item) for item in items]