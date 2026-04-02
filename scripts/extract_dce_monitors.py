import requests
import json
import os
import time
from dotenv import load_dotenv

# ── CONFIG ──────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")
DL_FILTER = "Digital-Operations-Datadog-Alerts@thomsonreuters.com"
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "dce_monitors_raw.json")
BASE_URL = "https://api.datadoghq.com"
# ────────────────────────────────────────────────────────

if not API_KEY or not APP_KEY:
    print("Error: DD_API_KEY and DD_APP_KEY must be set in your .env file.")
    exit(1)

os.makedirs(DATA_DIR, exist_ok=True)

headers = {"DD-API-KEY": API_KEY, "DD-APPLICATION-KEY": APP_KEY, "Content-Type": "application/json"}


def fetch_all_monitors():
    all_monitors = []
    page = 0
    per_page = 100
    total_pages = 1

    while page < total_pages:
        print(f"Fetching page {page + 1} of {total_pages}...")

        params = {"query": f'notification:"{DL_FILTER}"', "per_page": per_page, "page": page}

        response = requests.get(f"{BASE_URL}/api/v1/monitor/search", headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code} - {response.text}")
            break

        data = response.json()

        if page == 0:
            total_pages = data["metadata"]["page_count"]
            total_count = data["metadata"]["total_count"]
            print(f"Total monitors found: {total_count}")
            print(f"Total pages to fetch: {total_pages}")

        monitors = data.get("monitors", [])
        all_monitors.extend(monitors)
        print(f"  Collected {len(monitors)} monitors. Running total: {len(all_monitors)}")

        page += 1
        time.sleep(0.5)

    return all_monitors


if __name__ == "__main__":
    print("Starting DCE monitor extraction...")
    print(f"Filter: {DL_FILTER}\n")

    monitors = fetch_all_monitors()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(monitors, f, indent=2)

    print(f"\n✅ Done. {len(monitors)} monitors saved to {OUTPUT_FILE}")
