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

subreddit_pos_score = {}
subreddit_neg_score = {}

subreddit_comment_quantity = {}
corpus = []

start_time = time.time()

print("Reddit Sentiment Analysis Script")
print("Enter query to find general sentiment and related key phrases")

#Getting sums of sentiment from top relevant threads
query = input("query: ")
all_subreddits = reddit.subreddit("all")
query_results = all_subreddits.search(query, limit=5)
for submission in query_results:
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        polarity = sid.polarity_scores(comment.body)
        subreddit_id = comment.subreddit.display_name
        subreddit_comment_quantity[subreddit_id] = subreddit_comment_quantity.get(subreddit_id, 0) + 1
        pos_score += polarity['pos']
        subreddit_pos_score[subreddit_id] = subreddit_pos_score.get(subreddit_id, 0) + pos_score
        neut_score += polarity['neu']
        neg_score += polarity['neg']
        subreddit_neg_score[subreddit_id] = subreddit_neg_score.get(subreddit_id, 0) + neg_score
        corpus.append(comment.body)

#Getting Keywords
r = Rake()
r.extract_keywords_from_sentences(corpus)
ranked_phrases = r.get_ranked_phrases()

#Averaging across quantity of comments
for subreddit in subreddit_pos_score:
    subreddit_pos_score[subreddit] = subreddit_pos_score[subreddit]/subreddit_comment_quantity[subreddit]
for subreddit in subreddit_neg_score:
    subreddit_neg_score[subreddit] = subreddit_neg_score[subreddit]/subreddit_comment_quantity[subreddit]

most_positive_subreddit = max(subreddit_pos_score.keys(), key=(lambda key: subreddit_pos_score[key]))
most_negative_subreddit = max(subreddit_neg_score.keys(), key=(lambda key: subreddit_neg_score[key]))

end_time = time.time()

print("\nResults\n")
print("Time Elapsed:")
print("{0:.2f}".format(end_time - start_time) + " seconds")
print("Sentiment Ratio:")
print(str("{0:.2f}".format(100*pos_score/(pos_score + neg_score))) + "% Positive")
print("Most positive subreddit:")
print(most_positive_subreddit)
print("Most negative subreddit:")
print(most_negative_subreddit)

print("Key Phrases:")

# iterate through the first 10 legimate phrases
counter = 0
for phrase in ranked_phrases:
    if not(looksLikeLink(phrase)):
        print(phrase)
        counter += 1
    if counter == 10:
        break
