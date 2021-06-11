from fastapi import FastAPI
from routes.news import news


app = FastAPI()

app.include_router(news)