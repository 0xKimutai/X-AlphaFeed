import json
import os

def load_tweets():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # folder: utils/
    tweets_path = os.path.join(base_dir, "..", "..", "tweets.json")  # go two levels up
    tweets_path = os.path.normpath(tweets_path)

    if not os.path.exists(tweets_path):
        print(f"[WARN] tweets.json not found at {tweets_path}")
        return []

    with open(tweets_path, "r", encoding="utf-8") as f:
        return json.load(f)
