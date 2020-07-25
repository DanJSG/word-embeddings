from gensim.models import KeyedVectors, Word2Vec
from bbcscraper import BBCScraper
from crawler import Crawler
import re

new_model = Word2Vec([["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]], min_count=1)

crawler = Crawler("www.bbc.co.uk")
paths = crawler.start_crawling("/news", limit=50)
scraper = BBCScraper()
for path in paths:
    regex = re.compile(r"[0-9].*$")
    if regex.search(path) == None:
        print(path + " does not match article rule.")
        continue
    print(path + " matches article rule!")
    url = "https://www.bbc.co.uk" + path
    sentences = scraper.scrape_page(url)
    if sentences == None:
        print(url + " is not an article.")
        continue
    print("Training model from article at " + url)
    new_model.build_vocab(sentences, update=True)
    new_model.train(sentences=sentences, total_examples=new_model.corpus_count, epochs=new_model.epochs)


new_model.wv.save_word2vec_format("./models/model.txt", binary=False)
new_model.wv.save("./models/model.bin")
