import sys
import os
import time
from time import mktime
from datetime import datetime
import collections
import pickle
import random
import argparse
from shutil import copyfile
from collections import defaultdict
import glob

import matplotlib.pyplot as plt
import numpy as np

from utils import Config, safe_pickle_dump
import stopwords

# lets load the existing database to memory
try:
    print(Config.db_path)
    db = pickle.load(open(Config.db_path, 'rb'))
except Exception as e:
    print('error loading existing database:')
    print(e)
    print('starting from an empty database')
    db = {}

def get_full_paper_id(full_paper_id):
    return full_paper_id.split('/')[-1]

def get_paper_id_without_version(full_paper_id):
    return full_paper_id.split('/')[-1].split('v')[0]

assert get_full_paper_id('http://arxiv.org/abs/1804.03131v1') == '1804.03131v1'
assert get_paper_id_without_version('http://arxiv.org/abs/1804.03131v1') == '1804.03131'

full_id_to_title_dict = {get_full_paper_id(doc['id']): doc['title'] for k, doc in db.items()}
id_before_version_to_title_dict = {get_paper_id_without_version(doc['id']): doc['title'] for k, doc in db.items()}
unique_ids_before_version = set([get_paper_id_without_version(doc['id']) for k, doc in db.items()])

with open('full_paper_id_to_title_dict.pkl', 'wb') as f:
    pickle.dump(full_id_to_title_dict, f)


def get_latest_paper_identifier(list_of_paper_identifiers):
    version_nums = [paper_id.split('/')[-1].split('.pdf')[0].split('v')[-1]
                    for paper_id in list_of_paper_identifiers]
    index_of_highest_version_num = version_nums.index(max(version_nums))

    return list_of_paper_identifiers[index_of_highest_version_num]#.split('/')[-1]

# get latest version of all files
all_files = glob.glob('data/txt/*')

same_paper_dict = defaultdict(list)
# holds lists of different versions of said paper
# example key: value = '1712.01217': '1712.01217v1.pdf.txt'
count_found_with_title = 0
count_found_with_id_before_version = 0
count_of_papers_with_more_than_1_version = 0
for f in all_files:
    full_id = f.split('/')[-1].split('.pdf')[0]
    id_without_version = full_id.split('v')[0]
    same_paper_dict[id_without_version].append(full_id)
    if len(same_paper_dict[id_without_version]) > 1:
        count_of_papers_with_more_than_1_version += 1
    if id_before_version_to_title_dict.get(id_without_version):
        count_found_with_title += 1
    if full_id_to_title_dict.get(full_id):
        count_found_with_id_before_version += 1


for paper_id in same_paper_dict.keys():
    print(same_paper_dict[paper_id])
    latest_paper_fp = get_latest_paper_identifier(same_paper_dict[paper_id])

    src_path = 'data/txt/{}.pdf.txt'.format(latest_paper_fp)
    dst_path = 'data/final_version_paper_txt/{}.pdf.txt'.format(latest_paper_fp.split('/')[-1])
    print('Copying src_path: {} to dst_path: {}'.format(src_path, dst_path))
    copyfile(src_path, dst_path)

print('Number of text files: {}'.format(len(all_files)))
print('Number of paper entries in db: {}'.format(len(db.keys())))
print('Num unique identifiers before version: {}'.format(len(unique_ids_before_version)))
print('Num papers with final version: {}'.format(len(same_paper_dict)))
print('full_id_to_title_dict len: {}'.format(len(full_id_to_title_dict)))
print('count_found_with_id_before_version len: {}'.format(count_found_with_id_before_version))
print('count_found_with_title len: {}'.format(count_found_with_title))
print('count_of_papers_with_more_than_1_version len: {}'.format(count_of_papers_with_more_than_1_version))
print('{} - {} = {}'.format(count_found_with_title, count_found_with_id_before_version, count_found_with_title - count_found_with_id_before_version))
print('Num found with title: {}/{}'.format(count_found_with_title, len(all_files)))
