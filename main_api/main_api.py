from fastapi import FastAPI
from news import NewsApi
from scraper import ArticleScraper
from model_adapter import ModelAdapter


app = FastAPI()
news = NewsApi()
scraper = ArticleScraper()
model = ModelAdapter()


class TimelineElement:
    def __init__(self, article):
        self.content = scraper.get_article_content(article)
        self.pub_date = article["publishedAt"]
        self.url = article["url"]
        self.source = article["source"]["name"]

    @property
    def summary(self):
        return model.summarize(self.content)


@app.get("/topic/{topic}")
def get_topic(topic: str):
    articles = news.get_articles(topic)
    elements = [TimelineElement(article) for article in articles]
    timeline = [
        {
            "content": element.content,
            "summary": element.summary,
            "pub_date": element.pub_date,
            "url": element.url,
            "source": element.source,
        }
        for element in elements
    ]
    return timeline
