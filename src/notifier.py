import os
import requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CINEMARK_URL = "https://www.cinemark.com/movies/the-odyssey-imax-70mm"


def send_alert(new_dates: set[str]) -> None:
    dates_str = ", ".join(sorted(new_dates))
    requests.post(WEBHOOK_URL, json={
        "content": f"New Odyssey IMAX 70mm date(s) added: **{dates_str}**\n{CINEMARK_URL}"
    })
