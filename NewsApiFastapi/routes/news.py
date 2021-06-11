from fastapi import APIRouter

from models.news import News
from config.db import conn
from schemas.news import newEntity, newsEntity
from bson import ObjectId

news = APIRouter()

class NewsRouter:
    @news.get('/news/{id}')
    async def find_one_news(id):
        return newEntity(conn.NewsDB.News.find_one({"_id":ObjectId(id)}))

    @news.get('/news/')
    async def find_all_news(category : str="",limit :int = 0):
        if category != "" and limit != 0:
            return newsEntity(conn.NewsDB.News.find({"category":category}))[:limit]
        elif category != "":
            return newsEntity(conn.NewsDB.News.find({"category":category}))
        elif limit != 0:
            return newsEntity(conn.NewsDB.News.find())[:limit]
        return newsEntity(conn.NewsDB.News.find())

    @news.post('/news/')
    async def create_news(news:News):
        try: 
            if conn.NewsDB.News.find_one({"title":news.title}):
                return "news already in "
            conn.NewsDB.News.insert_one(dict(news))
            return "news successfully addd"
        except:
            return  "error"

    @news.put('/news/{id}')
    async def update_news(id,news:News):
        conn.NewsDB.News.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(news)})
        return newEntity(conn.NewsDB.News.find_one({"_id":ObjectId(id)}))

    @news.delete('/news/{id}')
    async def delete_news(id):
        conn.NewsDB.News.find_one_and_delete({"_id":ObjectId(id)})
        return "news successfully deleted"
