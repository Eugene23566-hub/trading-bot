# signal_sources/crypto_news.py

import requests

def get_market_sentiment():
    url = "https://cryptopanic.com/api/v1/posts/?kind=news&filter=hot"
    try:
        response = requests.get(url)
        data = response.json()
        score = 0

        for post in data.get("results", []):
            title = post.get("title", "").lower()
            if any(x in title for x in ["bullish", "surge", "pump", "positive"]):
                score += 1
            elif any(x in title for x in ["bearish", "crash", "dump", "negative"]):
                score -= 1

        if score > 1:
            return "bullish"
        elif score < -1:
            return "bearish"
        else:
            return "neutral"
    except Exception as e:
        print(f"[!] Ошибка при получении новостей: {e}")
        return "neutral"
