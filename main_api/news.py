from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

import os
from typing import TypedDict
from setup import sources


class Source(TypedDict):
    id: str
    name: str


class Article(TypedDict):
    source: Source
    author: str
    title: str
    description: str
    url: str
    urlToImage: str
    publishedAt: str
    content: str


class NewsApi:
    def __init__(self):
        api_key = os.getenv("NEWS_API_KEY")
        self.client = NewsApiClient(api_key)

    def get_articles(self, topic: str) -> list[Article] | dict:
        try:
            articles = self.client.get_everything(
                q=topic,
                sources=sources,
                language="en",
            )["articles"]
        except (NewsAPIException, KeyError) as e:
            return {"error": str(e)}
        return articles
