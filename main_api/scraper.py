from bs4 import BeautifulSoup
from setup import sources
from news import Article
import requests


class ScraperException(Exception):
    pass


class ArticleScraper:
    sources = sources.split(",")

    def get_article_content(self, article: Article) -> str:
        source = article["source"]["id"]
        if source not in self.sources:
            raise ScraperException("Source not supported")

        html = self.get_html(article["url"])

        match source:
            case "bbc-news":
                return self.bbc(html)

    def bbc(self, html: bytes) -> str:
        soup = BeautifulSoup(html, "html.parser")
        return soup.article.get_text()

    def get_html(self, url: str) -> bytes:
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ScraperException(f"Failed to fetch article: {e}")
        if response.status_code != 200:
            raise ScraperException(
                f"Failed to fetch article: Status {response.status_code}"
            )
        return response.content
