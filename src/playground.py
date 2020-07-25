from gensim.models import KeyedVectors, Word2Vec

model = Word2Vec.load("./models/fullmodel2.bin")

while True:
    word_in = input("Words similar to: ")
    similar = model.wv.most_similar(word_in)
    print(similar)
