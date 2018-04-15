import os
import time
from time import mktime
from datetime import datetime
import collections
import pickle
import random
import argparse
import urllib.request
import feedparser

import stopwords

import matplotlib.pyplot as plt
import numpy as np

from utils import Config, safe_pickle_dump

# lets load the existing database to memory
try:
    db = pickle.load(open(Config.db_path, 'rb'))
except Exception as e:
    print('error loading existing database:')
    print(e)
    print('starting from an empty database')
    db = {}

print(len(db.keys()))

# todo Get all RL paper titles from all time
# todo Simple tokenized keyword counting (fix problems) on all titles+abstracts
# todo Store all papers+titles in a cool JSON data structure with extra info
# todo Finish keyword counting with n-grams
# todo Do more complex Topic Modelling
# todo Links and even web page or slack bots to display everything easily
# todo Manually group each paper into an application area.
# todo Create Visualisations and stats. Bokeh, plotly or some other python tool?
# todo Write about it or list it somewhere
# todo start putting labels on each paper
# todo create RNN to generate paper
# todo create RNN for language modelling
# todo cluster documents
# todo tfidf on all docs and n-grams
# todo doc2vec
# todo search and information retrieval and
# todo look at karpathy's html
# todo get all papers back to start of 2014, download them all, get text for them all
# todo get mentions of all frameworks (TF, pytorch, etc)
# todo start categorising them all automatically
# todo start plotting the interest in certain techniques e.g. when was height of GAN fever? How many RL papers each month?
# todo topic modelling
# todo abstracts, titles and whole texts and their weight
# todo stemming? nltk tokenize? Remove words mentioned less than 3 times.
# todo automatic popularity testing. With twitter or through citations (Google Scholar)
# todo Automate everything


all_titles = [doc['title'] for k, doc in db.items() if doc['_version'] == 1]
all_dates = [datetime.fromtimestamp(mktime(doc['published_parsed'])) for k, doc in db.items() if doc['_version'] == 1]

print('Num papers counting all versions: {}. Num papers only first version: {}'.format(len(db.keys()), len(all_titles)))

# all_titles_words = [w for w in title.split() for title in all_titles]
# all_titles_words = [w for  in all_titles for title in ]
all_titles_words = [word.lower() for title in all_titles for word in title.split()]
all_titles_words = [word for word in all_titles_words if word not in stopwords.stopwords]
c = collections.Counter(all_titles_words)

for t in c.most_common(200):
    print(t)

dt_year = collections.defaultdict(list)
dt_month_in_year = collections.defaultdict(list)
for dt in all_dates:
    dt_year[str(dt.year)].append(dt)
    dt_month_in_year[str(dt.year) + '-' + str(dt.month)].append(dt)

x_ticks = []
num_in_each_year_month = []
for year in ['2015', '2016', '2017', '2018']:
# for year in ['2016', '2017']:#['2015', '2016', '2017', '2018']:
    print('\n', year, len(dt_year[year]), '\n')
    # dt_year[year].append()
    for month in range(1, 13):
        if year == '2018' and month == 5:
            break
        key = str(year) + '-' + str(month)
        num_in_year_month = len(dt_month_in_year[key])
        print(key, num_in_year_month)
        num_in_each_year_month.append(num_in_year_month)
        x_ticks.append(key[2:])


plt.plot(range(len(num_in_each_year_month)), num_in_each_year_month)
plt.xticks(range(len(num_in_each_year_month)), x_ticks, rotation='vertical')
plt.xlabel('Month')
plt.ylabel('Num papers')
plt.title('Num papers over time')
plt.grid(True)
# plt.savefig("test.png")
plt.show()
