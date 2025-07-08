# return all tweets
from fastapi import APIRouter
from app.utils.read_json import load_tweets

router = APIRouter()

@router.get("/feed")
def get_feed():
    tweets = load_tweets()
    return {"data": tweets}
