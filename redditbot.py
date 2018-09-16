import praw
from praw.models import MoreComments
import bs4
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import time
from config import client_id, client_secret, password, user_agent


file = open('input.txt', 'w')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     )

sid = SentimentIntensityAnalyzer()


pos_score = 0
neut_score = 0
neg_score = 0

start_time = time.time()

query = input("query: ")
all_subreddits = reddit.subreddit("all")
for submission in all_subreddits.search(query, limit=10):
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        polarity = sid.polarity_scores(comment.body)
        pos_score += polarity['pos']
        neut_score += polarity['neu']
        neg_score += polarity['neg']

end_time = time.time()

print("Sentiment Ratio:")
print(str((pos_score/(pos_score + neg_score))* 100) + "%")
print("Time Elapsed:")
print(end_time - start_time + " seconds")
"""
submission_links = []

# Finding the subreddits
if (len(links) > 0):
    for i in range(3):
        if links[i][-3:] == 'its':
            subreddit_links.append(links[i])

# Finding the submissions
for i in range (len(links)):
    if links[i][-3:] == 'sts':
        submission_links.append(links[i])


submission_keys = []

#Getting the unique submission 'keys' so they can be used with praw
for i in submission_links:
    ind = i.find("comments/") + 9
    submission_keys.append(i[ind:ind+6])

#Analyzing comment bodies for pos, neutral and negative scores
print("Processing Data")
if len(submission_keys) == 0:
    print('no submissions loaded')
    exit(0)

sid = SentimentIntensityAnalyzer()
positive = []
neutral = []
negative = []
for key in submission_keys:
    submission = reddit.submission(id=key)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        polarity = sid.polarity_scores(comment.body)
        positive.append(polarity['pos'])
        neutral.append(polarity['neu'])
        negative.append(polarity['neg'])

pos_avg = np.mean(positive)
neutral_avg = np.mean(neutral)
neg_avg = np.mean(negative)
print("Sentiment Analysis:")
print(pos_avg)
print(neutral_avg)
print(neg_avg)

print("Sentiment Ratio:")
print(str(pos_avg/neg_avg))
"""