import webbrowser
from datetime import date, timedelta, datetime


def main() -> None:
    today = date.today()
    interval = timedelta(days=30)

    end = today - interval
    end = datetime.combine(end, datetime.min.time())
    url = f"https://mail.proton.me/u/0/trash#end={int(end.timestamp())}"
    webbrowser.open(url)

    # Manually select trash from the last 30 days
    url = "https://drive.proton.me/u/0/trash"
    webbrowser.open(url)
