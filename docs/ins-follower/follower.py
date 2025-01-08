from bs4 import BeautifulSoup as bs
import urllib.request as urllib2
following = urllib2.urlopen('file:///C:/Users/13764/Downloads/following_page.html')
soup = bs(following)
ass = soup.find_all('a')
following_list = set()
for a in ass:
    a = str(a)
    #print(a)
    elements = a.split()
    for element in elements:
        if "href=" in element:
            print(element)
            username = element.split('/')[3]
            #print(username)
    following_list.add(username)

print(following_list)

"""
followers = urllib2.urlopen("file:///C:/Users/13764/Downloads/instagram-minggongd-2024-06-01-pWlRAIDB/connections/followers_and_following/followers_1.html")
soup = bs(followers)
ass = soup.find_all('a')
followers_list = []
for a in ass:
    a = str(a)
    elements = a.split('<')[1].split('>')[1]
    #print(elements)
    followers_list.append(elements)   

#print(following_list)
#print(followers_list) 
"""

followers = urllib2.urlopen('file:///C:/Users/13764/Downloads/followers_page.html')
soup = bs(followers)
ass = soup.find_all('a')
followers_list = set()
for a in ass:
    a = str(a)
    #print(a)
    elements = a.split()
    for element in elements:
        if "href=" in element:
            #print(element)
            username = element.split('/')[3]
            #print(username)
    followers_list.add(username)

print(followers_list)
count = 0
for f in following_list:
    if f not in followers_list:
        print(f)
        count += 1

print(count)
print(followers_list == following_list)