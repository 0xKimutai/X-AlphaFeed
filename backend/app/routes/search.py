# filter by query
from fastapi import APIRouter, Query
from app.utils.read_json import load_tweets

router = APIRouter()

@router.get("/search")
def search_feed(q: str = Query(..., min_length=1)):
    tweets = load_tweets()
    filtered = [tweet for tweet in tweets if q.lower() in tweet["snippet"].lower()]
    return {"data": filtered}
