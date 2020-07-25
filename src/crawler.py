from bs4 import BeautifulSoup
import requests

class Crawler:
    def __init__(self, domain_url):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        }
        self.domain_url = domain_url
        self.visited = []
        self.discovered = []
    
    def start_crawling(self, start_path, limit=250):
        url = "https://" + self.domain_url + start_path
        print("Fetching links from " + str(url))
        response = requests.get(url, self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=True)
        self.visited.append(start_path)
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
            url = "https://" + self.domain_url + curr_path
            print("Fetching links from " + str(url))
            response = requests.get(url, self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            links = soup.find_all('a', href=True)
            for link in links:
                if link['href'] == '' or link['href'][0] != '/' or (link['href'] in self.discovered) or (link['href'] in self.visited) or '.' in link['href']:
                    continue
                # print(link['href'])
                self.discovered.append(link['href'])
                if(len(self.discovered) >= limit):
                    break
            self.visited.append(curr_path)
            i += 1
        return self.discovered
        