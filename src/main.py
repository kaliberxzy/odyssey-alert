import json
import os
import schedule
import time
from dotenv import load_dotenv
from scraper import get_show_dates
from notifier import send_alert

load_dotenv()

KNOWN_DATES_FILE = "known_dates.json"


def load_known_dates() -> set[str]:
    if not os.path.exists(KNOWN_DATES_FILE):
        return None
    with open(KNOWN_DATES_FILE) as f:
        return set(json.load(f))


def save_known_dates(dates: set[str]) -> None:
    with open(KNOWN_DATES_FILE, "w") as f:
        json.dump(sorted(dates), f)


def check():
    current_dates = get_show_dates()
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


check()
schedule.every(5).minutes.do(check)

while True:
    schedule.run_pending()
    time.sleep(30)
