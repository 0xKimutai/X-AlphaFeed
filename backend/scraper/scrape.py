# scrape.py
# This script uses Bing to search for Twitter analysis links (no API, no login)
# It saves tweet link previews and URLs to tweets.json

from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime
from urllib.parse import quote

# Search keywords
KEYWORDS = ["$BTC analysis", "$ETH prediction", "#Solana crypto", "#stocks insights"]

# Number of links to collect per keyword
RESULTS_PER_KEYWORD = 5

# Output file
OUTPUT_FILE = "../tweets.json"

def scrape_bing_twitter_links():
    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for silent scraping
        context = browser.new_context()
        page = context.new_page()

        for keyword in KEYWORDS:
            print(f"🔍 Searching Bing for: {keyword}")
            query = f"site:twitter.com {keyword}"
            encoded_query = quote(query)
            search_url = f"https://www.bing.com/search?q={encoded_query}"

            try:
                page.goto(search_url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(5)

                # Scroll to help load more results
                page.mouse.wheel(0, 1000)
                time.sleep(2)

                # Select result links
                results = page.query_selector_all("li.b_algo h2 a")
                count = 0

                for r in results:
                    try:
                        link = r.get_attribute("href")
                        text = r.inner_text()

                        result = {
                            "keyword": keyword,
                            "snippet": text.strip(),
                            "url": link,
                            "timestamp": datetime.now().isoformat()
                        }

                        all_results.append(result)
                        count += 1

                        if count >= RESULTS_PER_KEYWORD:
                            break

                    except Exception as e:
                        print(f"❌ Error extracting link: {e}")
                        continue

            except Exception as e:
                print(f"❌ Bing search failed for {keyword}: {e}")
                continue

        browser.close()

    # Save results to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f"✅ Done. {len(all_results)} tweet links saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_bing_twitter_links()
