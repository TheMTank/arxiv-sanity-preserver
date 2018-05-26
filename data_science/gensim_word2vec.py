import time
import os
import sys
import collections

import gensim
from gensim.models.phrases import Phrases

data_dir = '../data/txt'
files = os.listdir(data_dir)
print(len(files))

def get_all_documents(n=100):
    all_documents = []
    for i in range(n):
        with open(data_dir + '/' + files[i]) as f:
            text_in_paper = f.readlines()
            text_in_paper = [l.lower().strip().split(' ') for l in text_in_paper]
            text_in_paper = [l for l in text_in_paper if len(l) > 0]
            #print(text_in_paper)
            #f
            for l in text_in_paper:
                if type(l) == list:
                    # print(l)
                    break
            all_documents.extend(text_in_paper)

    return all_documents

def calculate_counter(documents):
    flattened_list = [word for sentence in documents for word in sentence]
    # print(flattened_list[0:100])
    c = collections.Counter(flattened_list)

    for w_c in c.most_common(100):
        print(w_c)

documents = get_all_documents(1000)

# n-grams
start = time.time()
bigram_transformer = Phrases(documents)
bigram_docs = bigram_transformer[documents]
trigram_transformer = Phrases(bigram_docs)
trigram_docs = trigram_transformer[bigram_docs]

corpus = trigram_docs

calculate_counter(corpus)
print('Time taken to create n-grams: {}'.format(time.time() - start))

# create model
start = time.time()
model = gensim.models.Word2Vec(corpus, size=150, window=5, min_count=10, workers=4)
print('Time taken to create model: {}'.format(time.time() - start))

start = time.time()
model.train(corpus, total_examples=len(corpus), epochs=10)
# todo train per epoch and save model during each epoch
print('Time taken for training: {}'.format(time.time() - start))

for token in ['deep', 'deep_learning', 'artificial_intelligence']:
    if token in model.wv.vocab:
        print(model.wv.most_similar(positive=token))
    else:
        print(token, 'not in vocab')

print(model)

fp = 'models/gensim-word2vec-model-vocab-size-{}.pkl'.format(len(model.wv.vocab))
model.save(fp)

#model.score(["The fox jumped over a lazy dog".split()])

# model.wv.evaluate_word_pairs(os.path.join(module_path, 'test_data','wordsim353.tsv'))

