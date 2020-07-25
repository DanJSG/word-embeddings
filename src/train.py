from gensim.models import KeyedVectors, Word2Vec
from bbcscraper import BBCScraper
from crawler import Crawler
import re

new_model = Word2Vec([["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]], min_count=1)

crawler = Crawler("www.bbc.co.uk")
paths = crawler.start_crawling("/news", limit=10000)
scraper = BBCScraper()
count = 0
for path in paths:
    if count % 25 == 0 and count != 0:
        new_model.wv.save_word2vec_format("./models/model_partial.txt", binary=False)
        new_model.wv.save("./models/model_partial.bin")
        new_model.save("./models/model_partial_full.bin")
    count += 1
    regex = re.compile(r"[0-9].*$")
    if regex.search(path) == None:
        continue
    url = "https://www.bbc.co.uk" + path
    sentences = scraper.scrape_page(url)
    if sentences == None:
        continue
    print("Training model from article body of " + url + ". Training doc: " + str(count))
    new_model.build_vocab(sentences, update=True)
    new_model.train(sentences=sentences, total_examples=new_model.corpus_count, epochs=new_model.epochs)
    # update model every 25 
    if count % 25 == 0:
        new_model.wv.save_word2vec_format("./models/model_partial.txt", binary=False)
        new_model.wv.save("./models/model_partial.bin")
        new_model.save("./models/model_partial_full.bin")

new_model.wv.save_word2vec_format("./models/model2.txt", binary=False)
new_model.wv.save("./models/model2.bin")
new_model.save("./models/fullmodel2.bin")
