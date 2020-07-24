from bs4 import BeautifulSoup
import requests, re

class Scraper:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        }

    def scrape_page(self, url):
        response = requests.get(url, self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def _tokenize(self, content):
        sentences = re.compile(r'[^a-z0-9A-Z @\.\-\_]').sub('', content).lower().strip()
        sentences = re.compile('[ ]{2,}').sub(' ', sentences).strip().split(".")
        tokenized = []
        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split(" ")
            if len(words) == 1:
                continue
            tokenized.append(words)
        return tokenized
    
