import praw
import bs4
import requests
import os
# may need to import os

# Consider using a read only version of Reddit
file = open('input.txt', 'w')

reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     password='fakepassword',
                     user_agent='blank',
                     username='SentiSearchBot')
print(reddit.user.me())
# https://www.reddit.com/r/redditdev/search?q=hello+world+this+is+a+test&sort=relevance&t=all
# q= [SEARCH QUERY, spaces replaced by +, modify relevance to desired parameter
# &restrict_sr=on for specifying subreddit


# don't forget to block /r/circlejerk, bound to
# On second thought, let's not go to Circlelot, 'tis a silly place

query = input("query: ").replace(' ', '+')
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

#print(links[0])
#print(links[4])


subreddit_links = []
submission_links = []

# Finding the subreddits



for i in range(3):
    print(links[i])
    if links[i][-3:] == 'its':
        subreddit_links.append(links[i])

# Finding the submissions
for i in range (len(links)):
    if links[i][-3:] == 'sts':
        submission_links.append(links[i])

print(subreddit_links)

print(submission_links)

