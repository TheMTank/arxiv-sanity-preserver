import time
import os
import sys
import collections
import pickle

import gensim
from gensim.models.phrases import Phrases

import stopwords

data_dir = '../data/txt'
files = os.listdir(data_dir)
print('Num text files:', len(files))

from utils import Config, safe_pickle_dump

# lets load the existing database to memory
try:
    print(Config.db_path)
    db = pickle.load(open('../' + Config.db_path, 'rb'))
except Exception as e:
    print('error loading existing database:')
    print(e)
    print('starting from an empty database')
    db = {}

# todo read newest papers first

keys_in_1804 = [k for k in db.keys() if k[:4] == '1804']
print(len(keys_in_1804))
# sys.exit()

def get_all_documents(n=100):
    print('Reading ', n, ' files')
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
    print('Beginning counter')
    flattened_list = [word for sentence in documents for word in sentence]
    # print(flattened_list[0:100])
    c = collections.Counter(flattened_list)

    for w_c in c.most_common(2000):
        if w_c not in stopwords:
            print(w_c)

documents = get_all_documents(5000)

# n-grams
start = time.time()
bigram_transformer = Phrases(documents)
bigram_docs = bigram_transformer[documents]
trigram_transformer = Phrases(bigram_docs)
trigram_docs = trigram_transformer[bigram_docs]

corpus = trigram_docs
print('Time taken to create n-grams: {}'.format(time.time() - start))

start = time.time()
calculate_counter(corpus)
print('Time taken to run counter: {}'.format(time.time() - start))

# sys.exit()

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

