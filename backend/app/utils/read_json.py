#Utility to read tweets
import json
from pathlib import Path

def load_tweets():
    tweets_path = Path(__file__).resolve().parents[2] / "tweets.json"
    if not tweets_path.exists():
        return []
    with open(tweets_path, "r", encoding="utf-8") as f:
        return json.load(f)
