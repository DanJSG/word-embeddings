from gensim.models import KeyedVectors, Word2Vec
from bbcscraper import BBCScraper

scraper = BBCScraper()
# results = scraper.scrape_page("https://www.bbc.co.uk/news/uk-politics-52383444")
results = scraper.scrape_page("https://www.bbc.co.uk/news/world-europe-53529659")
for result in results:
    print(result)
# print(results)

# model = Word2Vec(['this', 'is', 'a', 'test', 'sentence'])

