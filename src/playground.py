from gensim.models import KeyedVectors, Word2Vec

model = KeyedVectors.load("./models/model.bin", mmap='r')
similar = model.most_similar("pm")
# similar = model.wv.most_similar("england")
print(similar)