from gensim.models import KeyedVectors, Word2Vec
from bbcarticle import BBCArticle
from wikiarticle import WikiArticle
from crawler import Crawler
import re

bbc_limit = 15
wiki_limit = 15

new_model = Word2Vec([["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]], min_count=1)

crawler = Crawler("https://en.wikipedia.org/wiki/Wikipedia:Contents/A%E2%80%93Z_index")
paths = crawler.crawl(limit=wiki_limit)
count = 0
trained_count = 0

for path in paths:
    if count % 25 == 0 and count != 0:
        new_model.wv.save_word2vec_format("./models/model_partial.txt", binary=False)
        new_model.wv.save("./models/model_partial.bin")
        new_model.save("./models/model_partial_full.bin")
    count += 1
    url = crawler.protocol + crawler.domain + path
    scraper = WikiArticle(url)
    if scraper.sentences == None:
        continue
    trained_count += 1
    print("Training model from article body of " + url + ". Page count: " + str(count) + ". Training document: " + str(trained_count))
    new_model.build_vocab(scraper.sentences, update=True)
    new_model.train(sentences=scraper.sentences, total_examples=new_model.corpus_count, epochs=new_model.epochs)

crawler = Crawler("https://www.bbc.co.uk/news")
paths = crawler.crawl(limit=bbc_limit)

for path in paths:
    if count % 25 == 0 and count != 0:
        new_model.wv.save_word2vec_format("./models/model_partial.txt", binary=False)
        new_model.wv.save("./models/model_partial.bin")
        new_model.save("./models/model_partial_full.bin")
    count += 1
    regex = re.compile(r"[0-9].*$")
    if regex.search(path) == None:
        continue
    url = crawler.protocol + crawler.domain + path
    scraper = BBCArticle(url)
    if scraper.sentences == None:
        continue
    trained_count += 1
    print("Training model from article body of " + url + ". Page count: " + str(count) + ". Training document: " + str(trained_count))
    new_model.build_vocab(scraper.sentences, update=True)
    new_model.train(sentences=scraper.sentences, total_examples=new_model.corpus_count, epochs=new_model.epochs)

new_model.wv.save_word2vec_format("./models/model2.txt", binary=False)
new_model.wv.save("./models/model2.bin")
new_model.save("./models/fullmodel2.bin")
