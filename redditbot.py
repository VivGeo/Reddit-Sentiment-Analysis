import praw
from praw.models import MoreComments
import bs4
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
file = open('input.txt', 'w')

reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     password='fakepassword',
                     user_agent='blank',
                     )
print(reddit.user.me())

query = input("query: ").replace(' ', '+')
print(" ")
page = requests.get('https://www.reddit.com/r/all/search?q=' + query + '&sort=relevance&t=all')
soup = bs4.BeautifulSoup(page.text,"html.parser")
linkElems = soup.select('header[class="search-result-header"] > a')
# print(len((linkElems)))

# scrub input (necessary for things to work)
for elem in linkElems:
    file.write(elem.get('href') + "\n")
file.close()

links = []
file2 = open('input.txt', 'r')
for line in file2:
    links.append(file2.readline()[:-1])

file2.close()

subreddit_links = []
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
