from fastapi import FastAPI
from news import NewsApi
from scraper import ArticleScraper
from logs import setup_logger

setup_logger()
app = FastAPI()
news = NewsApi()
scraper = ArticleScraper()


class TimelineElement:
    def __init__(self, article):
        self.content = scraper.get_article_content(article)
        self.pub_date = article["publishedAt"]
        self.url = article["url"]
        self.source = article["source"]["name"]



@app.get("/topic/{topic}")
def get_topic(topic: str):
    articles = news.get_articles(topic)
    elements = [TimelineElement(article) for article in articles]
    timeline = [
        {
            "pub_date": element.pub_date,
            "url": element.url,
            "source": element.source,
            "content": element.content
        }
        for element in elements
    ]
    return [entry for entry in timeline if entry["content"]]
