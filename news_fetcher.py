import feedparser

def get_google_news_rss(ticker, limit=20):
    query = ticker.replace(" ", "+")
    feed_url = f"https://news.google.com/rss/search?q={query}+stock&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return []

    return [
        f"{i+1}. {entry.title.strip()}"
        for i, entry in enumerate(feed.entries[:limit])
    ]
