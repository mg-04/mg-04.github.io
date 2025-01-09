---
layout: post
title:  "Instagram Follower Manager"
date:   2025-1-7 22:03:30 -0500
categories: code
---
A script to find the set of Instagram followers that don't follow you back

> Yes, I am jealous, bored, insecure, a horrible person, and whatever you wish to name me.

Instagram lists your followers you don't follow back, but not the opposite. The reason is obvious: Meta want you to follow more people back, instead of being a rat and unfollowing those that don't.

The conventional way is to download and process Instagram analytics: https://www.reddit.com/r/Instagram/comments/yhazli/how_to_see_who_is_not_following_you_back_without/

However, these data take a while to arrive. I seek to find a faster way: scraping the ins website and find a set of all the followers and following. 

> Lots of the code framework are from chatGPT. I'm a complete noob in web scraping, but it just shows how AI can greatly simplify our learning curve in application.

# V1. `BeautifulSoup`

I wrote this version using `BeautifulSoup` a few months ago, where I first loaded the ins pages all the way to the end, downloaded the html files, and let `bs4` do its job.

https://github.com/mg-04/mg-04.github.io/blob/main/docs/ins-follower/follower.py

Each of the list elements have `<a>` hyperlinks, so the code basically extracts all of them, and compares the set. 

Instagram does not load the full following list after clicking the link (because there is too many to load). After you scroll to the bottom, it will load some additional content. This process needs to be repeated until the end is reached.

# V2. Auto Scroller

As I gain more followers, however, this process of obtaining the html document becomes longer and longer, and I'm looking for a script to automate this. Again, chatgpt for the save. 

Instagram's html elements are heavily obfuscated, and we need to `F12` the elements to locate their classes. 

https://github.com/mg-04/mg-04.github.io/blob/main/docs/ins-follower/autoscroll.py

I used `selenium` for the web driver. The steps are follows:
1. Log in to Instagram (This can be skipped if I allow the driver to test under my Chrome profile)
2. Click the "Followers" button 
    - Locate the `<a>` element with keyword "Followers"
    - Click the button and wait for the page to load
3. Locate the `dialog` element, whose class name contains "xyi19xy"
4. Scroll to the bottom of the dialog
    - until the height of the dialog element no longer changes

Now we have automatically loaded the html file. It's time to process it
- We can technically download it, and use the old `bs` code from that point, but we can also use `Selenium` to find the elements containing the usernames.

5. Locate the `<div>` elements
    - class name containing "x1dm5mii"
6. Extract usernames from the elements
    - Look for the `<a>` tags linking to usernames, and extract their `href` URL
7. Compile all followers and following to a `set`, and compare the usernames.

# Usage

To use it, simply input your username and password (of course I won't steal it)

Let's test it on minggongdd:
```python
# Instagram credentials
USERNAME = "minggongdd"
PASSWORD = "password"
```

and hit run!

![log in page](/images/login.png)
![followers](/images/followers.png)
![following](/images/following.png)

and here's the list:

![result](/images/result.png)

## Obfuscated HTML elements
As mentioned before, some of the element class search keywords may become invalid after certain Instagram updates. If Selenium fails to locate any element, it will throw an error message, and you'll need to `F12` the webpage and find the updated class names for that element.