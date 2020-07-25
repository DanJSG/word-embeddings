from bs4 import BeautifulSoup
from article import Article
import requests, re

class WikiArticle(Article):
    def __init__(self, url):
        super().__init__(url)
        self.body = self._scrape_page()
        self.sentences = self._tokenize(self.body)
    
    def _scrape_page(self) -> str:
        try:
            response = requests.get(self.url, self.headers)
        except:
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        article = soup.find(id="bodyContent")
        if article == None:
            return None
        paras = article.find_all('p')
        text = ""
        for para in paras:
            if para.has_attr("aria-hidden"):
                continue
            text += para.get_text()
        return text
    