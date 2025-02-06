from fastapi.testclient import TestClient
from main_api.main_api import app
from news import NewsApi
from scraper import ArticleScraper
from model_adapter import ModelAdapter


class MainTest:
    def setup(self):
        self.news_api = NewsApi()
        self.article_scraper = ArticleScraper()
        self.summary_api = ModelAdapter()
        self.client = TestClient(app)

    def test_get_articles_for_topic(self):
        topic = "bitcoin"
        response = self.client.get(f"/topic/{topic}")
        assert response.status_code == 200
