import httpx
from bs4 import BeautifulSoup


async def fetch_contributions(username: str, from_date: str | None = None, to_date: str | None = None) -> list[dict]:
    url = f"https://github.com/users/{username}/contributions"
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, follow_redirects=True)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    contributions = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level")
        if date and level is not None:
            contributions.append({"date": date, "level": int(level)})

    contributions.sort(key=lambda x: x["date"])
    return contributions
