import argparse
import json
import re
import warnings
import zoneinfo
from collections.abc import Generator, Sequence
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_schedules(lang: str, timezone: str) -> Generator[dict, None, None]:
    URL = f"https://atcoder.jp/contests/?lang={lang}"
    soup = BeautifulSoup(requests.get(URL).text, "lxml")
    table = soup.select_one("#contest-table-upcoming tbody")
    for tr in table.find_all("tr"):
        try:
            # Fix timezone format for python<3.11
            time_text = tr.select_one("td:nth-of-type(1) time").text
            time_text = re.sub(r"(\+\d\d)(\d\d)$", r"\1:\2", time_text)
            dt = datetime.fromisoformat(time_text)
            tz = zoneinfo.ZoneInfo(timezone)
            contest_link = tr.select_one("td:nth-of-type(2) a")
            data = {
                "start_time": dt.astimezone(tz).isoformat(),
                "timestamp": int(dt.timestamp()),
                "name": contest_link.text,
                "url": urljoin(URL, contest_link["href"]),
                "duration": tr.select_one("td:nth-of-type(3)").text,
                "rated_range": tr.select_one("td:nth-of-type(4)").text,
            }
            yield data
        except Exception as e:
            warnings.warn(f"Error parsing row: {e}", stacklevel=2)
            continue


def cli(args: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Get upcoming AtCoder contests")
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="ja",
        choices=["ja", "en"],
        help="Language for the contest page",
    )
    parser.add_argument(
        "-z",
        "--timezone",
        type=str,
        default="Asia/Tokyo",
        help="Timezone for the contest start time",
    )
    _args = parser.parse_args(args)
    for contest in parse_schedules(_args.lang, _args.timezone):
        print(json.dumps(contest, ensure_ascii=False))


if __name__ == "__main__":
    cli()
