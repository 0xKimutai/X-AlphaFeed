# scrape.py
#  Scrapes Twitter analysis links using Bing search (no Twitter API or login)
#  Dynamically fetches crypto, forex, and stock symbols as keywords
#  Extracts tweet preview snippets and URLs into backend/tweets.json

import json
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime


# ------------------- SYMBOL FETCHERS -------------------

#  Fetches a list of crypto symbols (e.g., BTC, ETH) from CoinGecko
def get_crypto_symbols():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return list(set(coin['symbol'].upper() for coin in data if 'symbol' in coin))
    except Exception as e:
        print("⚠️ Error fetching crypto symbols:", e)
        return []

#  Fetches a list of forex currency codes (e.g., USD, EUR) from exchangerate.host
'''def get_forex_symbols():
    url = "https://api.exchangerate.host/symbols"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return list(data["symbols"].keys())
    except Exception as e:
        print("⚠️ Error fetching forex symbols:", e)
        return []
'''
def get_forex_symbols():
    return [
        "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "NZD",
        "ZAR", "KES", "NGN", "CNY", "HKD", "SGD"
    ]


#  Returns a static sample list of popular stock tickers
#  Can later replace this with a dynamic fetch from Yahoo Finance or similar
def get_stock_tickers():
    return ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NVDA", "META", "NFLX"]

#  Aggregates all asset symbols into one unique keyword list
def get_all_asset_keywords():
    crypto = get_crypto_symbols()
    forex = get_forex_symbols()
    stocks = get_stock_tickers()
    return list(set(crypto + forex + stocks))


# ------------------- MAIN SCRAPER FUNCTION -------------------

def scrape_bing_twitter_links():
    # Step 1: Collect asset keywords
    keywords = get_all_asset_keywords()
    print(f"📊 Fetched {len(keywords)} asset keywords to search for.")

    # Step 2: Set up browser context (headless = True for automation)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_results = []

        # Step 3: Loop through each keyword (limit to 100 for faster scraping)
        for keyword in keywords[:100]:
            query = f"{keyword} site:twitter.com"
            print(f"🔍 Searching: {query}")

            try:
                # Step 4: Search on Bing for tweets related to the keyword
                page.goto(f"https://www.bing.com/search?q={query}", timeout=15000)
                page.wait_for_timeout(3000)

                # Step 5: Parse results with BeautifulSoup
                soup = BeautifulSoup(page.content(), "html.parser")
                links = soup.find_all("a")

                for link in links:
                    href = link.get("href")
                    if href and "twitter.com" in href and "/status/" in href:
                        snippet = link.text.strip()
                        if snippet:
                            all_results.append({
                                "url": href,
                                "snippet": snippet,
                                "symbol": keyword,
                                "likes": 0,         # Placeholder
                                "comments": 0,      # Placeholder
                                "timestamp": datetime.utcnow().isoformat()
                            })
            except Exception as e:
                print(f"❌ Error scraping {keyword}: {e}")
                continue

        # Step 6: Save results to JSON
        browser.close()
        with open("backend/tweets.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"✅ Finished. Scraped {len(all_results)} tweets and saved to tweets.json.")


# ------------------- SCRIPT ENTRY POINT -------------------

if __name__ == "__main__":
    scrape_bing_twitter_links()
