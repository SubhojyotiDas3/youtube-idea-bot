import requests
import feedparser
import re
from collections import Counter

# -------- DIRECT TOKEN (NO SECRETS) --------
BOT_TOKEN = 8206593845:AAGIZjDS2sX0UbG4aIeRCdLzKPLtHA3H8Nw
CHAT_ID = 512451262

message = "🔥 Tech Content Ideas\n\n"

# ---------------- NEWS ----------------
message += "📰 Tech News\n"
news_feed = feedparser.parse("https://techcrunch.com/feed/")

for entry in news_feed.entries[:3]:
    message += "- " + entry.title + "\n"

# ---------------- YOUTUBE CHANNELS ----------------
message += "\n📺 YouTube Trends\n"

youtube_channels = [
"https://www.youtube.com/feeds/videos.xml?channel_id=UCXUJJNoP1QupwsYIWFXmsZg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCs0kMbzhUYV2lhIV7xoWhoA",
"https://www.youtube.com/feeds/videos.xml?channel_id=UC9x0AN7BWHpCDHSm9NiJFJQ",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCw5hEVOTfz_AfzsNFWyNlNg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCQteghH9BA1xQZ2v4hM9xRw",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCVYamHliCI9rw1tHR1xbkfw",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCdBK94H6oZT2Q7l0-b0xmMg",
"https://www.youtube.com/feeds/videos.xml?channel_id=UC0vBXGSyV14uvJ4hECDOl0Q",
"https://www.youtube.com/feeds/videos.xml?channel_id=UCXuqSBlHAE6Xw-yeJA0Tunw"
]

titles = []

for url in youtube_channels:
    feed = feedparser.parse(url)

    for entry in feed.entries[:2]:
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
