import json
import os
import sys
import schedule
import time
import argparse
from dotenv import load_dotenv
from scraper import get_show_dates
from notifier import send_alert

load_dotenv()

KNOWN_DATES_FILE = "known_dates.json"

def load_known_dates() -> set[str] | None:
    if not os.path.exists(KNOWN_DATES_FILE):
        return None
    with open(KNOWN_DATES_FILE) as f:
        return set(json.load(f))

def save_known_dates(dates: set[str]) -> None:
    with open(KNOWN_DATES_FILE, "w") as f:
        json.dump(sorted(dates), f)

def check():
    print("Fetching show dates...")
    try:
        current_dates = get_show_dates()
    except Exception as e:
        print(f"Scraper failed: {e}")
        return

    if not current_dates:
        print("Scraper returned no dates – skipping update.")
        return

    known_dates = load_known_dates()
    if known_dates is None:
        print(f"First run — seeding with {len(current_dates)} dates.")
        save_known_dates(current_dates)
        return

    new_dates = current_dates - known_dates
    if new_dates:
        print(f"New dates found: {new_dates}")
        send_alert(new_dates)
        save_known_dates(current_dates)
    else:
        print("No new dates.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run a single check and exit")
    args = parser.parse_args()

    if args.once:
        check()
    else:
        # Daemon mode – run once at startup, then every 5 minutes
        check()
        schedule.every(5).minutes.do(check)
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)
        except KeyboardInterrupt:
            print("Shutting down gracefully.")