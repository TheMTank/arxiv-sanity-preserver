import os
import sys
import collections

import gensim

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

calculate_counter(documents)


model = gensim.models.Word2Vec(documents, size=150, window=5, min_count=5, workers=4)


model.train(documents, total_examples=len(documents), epochs=10)

print(model.wv.most_similar(positive='deep'))

print(model)
print(model['deep'])

#model.score(["The fox jumped over a lazy dog".split()])

# model.wv.evaluate_word_pairs(os.path.join(module_path, 'test_data','wordsim353.tsv'))

