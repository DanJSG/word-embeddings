from bs4 import BeautifulSoup
import requests, re

class Article:
    def __init__(self, url):
        self.url = url
        self.protocol, self.domain, self.path = self._split_url(url)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        }

    def _split_url(self, url):
        reg_match = re.compile(r'(^https?://)([a-zA-Z.\-]*)(/.*)').match(url)
        protocol = reg_match.group(1)
        domain = reg_match.group(2)
        path = reg_match.group(3)
        return protocol, domain, path

    def _tokenize(self, content):
        if content == None:
            return None
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
    
