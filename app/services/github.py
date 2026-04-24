import asyncio
import re

import httpx
from bs4 import BeautifulSoup

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9\-]+$")

_client: httpx.AsyncClient | None = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(follow_redirects=True)
    return _client


def _parse_contributions(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    contributions = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level")
        if date and level is not None:
            contributions.append({"date": date, "level": int(level)})
    return contributions


async def _fetch_year(client: httpx.AsyncClient, url: str, params: dict | None = None) -> list[dict]:
    resp = await client.get(url, params=params)
    resp.raise_for_status()
    return _parse_contributions(resp.text)


async def fetch_contributions(username: str, from_date: str | None = None, to_date: str | None = None) -> list[dict]:
    if not USERNAME_PATTERN.match(username):
        return []

    url = f"https://github.com/users/{username}/contributions"
    client = get_client()

    # Figure out which years we need to fetch
    if from_date and to_date:
        from_year = int(from_date[:4])
        to_year = int(to_date[:4])
        years = list(range(from_year, to_year + 1))
    elif from_date:
        years = [int(from_date[:4])]
    else:
        years = []

    all_contributions: dict[str, dict] = {}

    try:
        if not years:
            for c in await _fetch_year(client, url):
                all_contributions[c["date"]] = c
        else:
            results = await asyncio.gather(
                *[_fetch_year(client, url, {"from": f"{year}-01-01"}) for year in years]
            )
            for year_data in results:
                for c in year_data:
                    all_contributions[c["date"]] = c
    except httpx.HTTPStatusError:
        return []

    result = sorted(all_contributions.values(), key=lambda x: x["date"])

    if from_date:
        result = [c for c in result if c["date"] >= from_date]
    if to_date:
        result = [c for c in result if c["date"] <= to_date]

    return result
