import tweepy
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import elastic_model

api_key = "2NK29wK3A5ifgSlaAGK0V13V5"
api_secret_key = "5ySd995z1D65VD0xn5eBjKa6ZpFREduib8aaCRW4sbQ7BknpAL"

access_token = "998211926596444165-DKSHFv8Tt7MJ5MREV2XjLq5Chz2n5yc"
access_token_secret = "1JRHchfJRafXKdIxt147YkJB4WteTrstTF3SjwEndXlq8"



auth = tweepy.auth.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

connections.create_connection(hosts=['localhost'])


client = Elasticsearch()
s = Search(using=client).filter('range', date={'gte': 'now-16d/d', 'lt': 'now-7d/d'})

print("Zerooing Papers!")
for res in s.scan():
    paper_id = res.meta.id
    article = elastic_model.Paper.get(id=paper_id)
    article.update(twitter_popularity=0)


s = Search(using=client).filter('range', date={'gte': 'now-7d/d', 'lt': 'now/d'})

print("Updating Papers!")
for res in s.scan():
    paper_id = res.meta.id
    splitted = paper_id.split("v")
    twitter_popularity = 0
    if len(splitted) == 2:
        search_results = api.search(q=paper_id.split("v")[0], count=100)
        twitter_popularity = len(search_results)

    search_results = api.search(q=paper_id, count=100)
    twitter_popularity = len(search_results)
    if twitter_popularity != 0:
        print(paper_id, twitter_popularity)
    article = elastic_model.Paper.get(id=paper_id)
    article.update(twitter_popularity=twitter_popularity)



