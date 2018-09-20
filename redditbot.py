import praw
from praw.models import MoreComments
import bs4
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rake_nltk import Metric, Rake
import numpy as np
import time
import itertools
from config import client_id, client_secret, password, user_agent

def looksLikeLink(phrase):
    if ("http" in phrase):
        return True
    else:
        return False

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     )

sid = SentimentIntensityAnalyzer()

pos_score = 0
neut_score = 0
neg_score = 0

corpus = []

start_time = time.time()

print("Reddit Sentiment Analysis Script")
print("Enter query to find general sentiment and related key phrases")

query = input("query: ")
all_subreddits = reddit.subreddit("all")
query_results = all_subreddits.search(query, limit=10)
for submission in query_results:
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        polarity = sid.polarity_scores(comment.body)
        pos_score += polarity['pos']
        neut_score += polarity['neu']
        neg_score += polarity['neg']
        corpus.append(comment.body)

r = Rake()
r.extract_keywords_from_sentences(corpus)
ranked_phrases = r.get_ranked_phrases()


end_time = time.time()



print("\nResults\n")
print("Sentiment Ratio:")
print(str("{0:.2f}".format(100*pos_score/(pos_score + neg_score))) + "% Positive")
print("Time Elapsed:")
print("{0:.2f}".format(end_time - start_time) + " seconds")
print("Key Phrases:")

# iterate through the first 10 legimate phrases
counter = 0
for phrase in ranked_phrases:
    if not(looksLikeLink(phrase)):
        print(phrase)
        counter += 1
    if counter == 10:
        break



