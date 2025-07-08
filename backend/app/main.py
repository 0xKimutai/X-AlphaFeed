# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import feed, search

# ✅ This must exist — Uvicorn looks for this variable
app = FastAPI()

# Allow CORS (so frontend can connect to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API endpoints
app.include_router(feed.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "X-Alpha backend is running 🚀"}
