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


# don't forget to block /r/circlejerk, bound to skew results
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

file2 = open('input.txt','r')
print(type(file2))

file2.close()

end = input("")
