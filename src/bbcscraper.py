from bs4 import BeautifulSoup
import requests
import re
from scraper import Scraper

class BBCScraper(Scraper):
    def __init__(self):
        super().__init__()
    
    def scrape_page(self, url) -> list:
        response = requests.get(url, self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        # article = soup.find(class_="story-body")
        article = soup.find(property="articleBody")
        if article == None:
            return None
        paras = article.find_all('p')
        text = ""
        for para in paras:
            if para.has_attr("aria-hidden"):
                continue
            text += para.get_text()
        return self._tokenize(text)
    