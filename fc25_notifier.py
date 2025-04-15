import requests
from bs4 import BeautifulSoup
import json
import time
import os

# === CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.ea.com/games/ea-sports-fc/fc-25/news?page=1&type=game-updates"
CHECK_INTERVAL = 60 * 60  # vérifie toutes les heures

def get_latest_article_title():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("a", class_="ea-article-tile")
    if article:
        return article.get_text(strip=True)
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def load_last_title():
    try:
        with open("last_title.json", "r") as f:
            return json.load(f).get("title")
    except FileNotFoundError:
        return None

def save_last_title(title):
    with open("last_title.json", "w") as f:
        json.dump({"title": title}, f)

def main():
    latest_title = get_latest_article_title()
    if latest_title:
        last_title = load_last_title()
        if latest_title != last_title:
            send_telegram_message(f"NOUVEL ARTICLE EA FC25 :\n{latest_title}")
            save_last_title(latest_title)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(CHECK_INTERVAL)
