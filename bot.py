import requests
import feedparser
import re
from collections import Counter
import os

# -------- SECURE TOKENS (FROM GITHUB SECRETS) --------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = "🔥 Tech Content Ideas\n\n"

# ---------------- NEWS ----------------
message += "📰 Tech News\n"
news_feed = feedparser.parse("https://techcrunch.com/feed/")

for entry in news_feed.entries[:3]:
    message += "- " + entry.title + "\n"


# ---------------- YOUTUBE CHANNELS ----------------
message += "\n📺 YouTube Trends\n"

youtube_channels = [

# YOUR + ADDED CHANNELS
"https://www.youtube.com/feeds/videos.xml?channel_id=UCkYJ2R0H7XrQ7b9K1gZ1p5g",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCqK1CkMZpS5z2PzZ7bX8k8A",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCg8xj3QXz3d7l6nF0cX4P2g",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCd8kZx3R7X6n9Y3kX5p2W1g",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCz9P3F7l2k5sX8m2V9n1c0Q",
"https://www.youtube.com/feeds/videos.xml?channel_id=UC4sEmXUuWIFlxRIFBRV6VXQ",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCkV1pX9f6Jw2l8mQ7b3h2sA",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCp8Xk3F5l9s2X7g1V6n2m3A",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCs8Jk7L2mX5p9F3b7c2V1gA",

# STRONG CHANNELS
"https://www.youtube.com/feeds/videos.xml?channel_id=UCXUJJNoP1QupwsYIWFXmsZg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCs0kMbzhUYV2lhIV7xoWhoA",
"https://www.youtube.com/feeds/videos.xml?channel_id=UC9x0AN7BWHpCDHSm9NiJFJQ",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCw5hEVOTfz_AfzsNFWyNlNg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCQteghH9BA1xQZ2v4hM9xRw",

# ENGLISH (LIMITED)
"https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCVYamHliCI9rw1tHR1xbkfw",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCdBK94H6oZT2Q7l0-b0xmMg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UC0vBXGSyV14uvJ4hECDOl0Q",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCXuqSBlHAE6Xw-yeJA0Tunw"

]

titles = []

for url in youtube_channels:
    feed = feedparser.parse(url)

    for entry in feed.entries[:2]:  # IMPORTANT: keep it small
        message += "▶ " + entry.title + "\n"
        titles.append(entry.title)


# ---------------- TREND DETECTOR ----------------
words = []

for title in titles:
    words += re.findall(r'\w+', title.lower())

common = Counter(words).most_common(10)

message += "\n🔥 Trending Keywords\n"

for word, count in common:
    if len(word) > 3:
        message += f"{word} ({count})\n"


# ---------------- REDDIT ----------------
message += "\n💬 Reddit Trends\n"

reddit_url = "https://www.reddit.com/r/technology/top.json?limit=5&t=day"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(reddit_url, headers=headers)

if response.status_code == 200:
    data = response.json()

    for post in data["data"]["children"]:
        message += "- " + post["data"]["title"] + "\n"
else:
    message += "Reddit fetch failed\n"


# ---------------- SEND TO TELEGRAM ----------------
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})
