from bs4 import BeautifulSoup
import requests, re

class Crawler:
    def __init__(self, url):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        }
        self.protocol, self.domain, self.start_path = self._split_url(url)
        self.visited = []
        self.discovered = []
    
    def _split_url(self, url):
        reg_match = re.compile(r'(^https?://)([a-zA-Z.\-]*)(/.*)').match(url)
        protocol = reg_match.group(1)
        domain = reg_match.group(2)
        path = reg_match.group(3)
        return protocol, domain, path

    def crawl(self, limit=50):
        url = self.protocol + self.domain + self.start_path
        print("Fetching links from " + str(url))
        response = requests.get(url, self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=True)
        self.visited.append(self.start_path)
        for link in links:
            if link['href'] == '' or link['href'][0] != '/' or (link['href'] in self.discovered) or '.' in link['href']:
                continue
            self.discovered.append(link['href'])
            if len(self.discovered) >= limit:
                break
        i = 0
        while len(self.discovered) < limit and i < len(self.discovered):
            curr_path = self.discovered[i]
            if curr_path in self.visited:
                i += 1
                continue
            url = self.protocol + self.domain + curr_path
            print("Fetching links from " + str(url))
            response = requests.get(url, self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            links = soup.find_all('a', href=True)
            for link in links:
                if link['href'] == '' or link['href'][0] != '/' or (link['href'] in self.discovered) or (link['href'] in self.visited) or '.' in link['href']:
                    continue
                self.discovered.append(link['href'])
                if(len(self.discovered) >= limit):
                    break
            self.visited.append(curr_path)
            i += 1
        return self.discovered
