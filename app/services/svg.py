from app.services.colors import DEFAULT_COLORS

CELL_SIZE = 11
CELL_GAP = 2
CELL_STEP = CELL_SIZE + CELL_GAP
MONTH_LABEL_HEIGHT = 15
DAY_LABEL_WIDTH = 28

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}


def generate_svg(contributions: list[dict], colors: list[str] = DEFAULT_COLORS) -> str:
    if not contributions:
        return '<svg xmlns="http://www.w3.org/2000/svg"></svg>'

    weeks: list[list[dict | None]] = []
    current_week: list[dict | None] = []

    from datetime import datetime

    first_date = datetime.strptime(contributions[0]["date"], "%Y-%m-%d")
    first_dow_sun = (first_date.weekday() + 1) % 7
    current_week = [None] * first_dow_sun

    for entry in contributions:
        d = datetime.strptime(entry["date"], "%Y-%m-%d")
        dow_sun = (d.weekday() + 1) % 7
        if dow_sun == 0 and current_week:
            while len(current_week) < 7:
                current_week.append(None)
            weeks.append(current_week)
            current_week = []
        current_week.append(entry)

    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)

    num_weeks = len(weeks)
    width = DAY_LABEL_WIDTH + num_weeks * CELL_STEP
    height = MONTH_LABEL_HEIGHT + 7 * CELL_STEP

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;font-size:10px">'
    ]

    month_positions: dict[str, int] = {}
    for wi, week in enumerate(weeks):
        for entry in week:
            if entry is None:
                continue
            d = datetime.strptime(entry["date"], "%Y-%m-%d")
            key = f"{d.year}-{d.month}"
            if key not in month_positions:
                month_positions[key] = wi
            break

    for key, wi in month_positions.items():
        year, month = key.split("-")
        x = DAY_LABEL_WIDTH + wi * CELL_STEP
        parts.append(
            f'<text x="{x}" y="10" fill="#767676">{MONTH_NAMES[int(month) - 1]}</text>'
        )

    for dow, label in DAY_LABELS.items():
        y = MONTH_LABEL_HEIGHT + dow * CELL_STEP + 9
        parts.append(f'<text x="0" y="{y}" fill="#767676">{label}</text>')

    for wi, week in enumerate(weeks):
        for di, entry in enumerate(week):
            if entry is None:
                continue
            x = DAY_LABEL_WIDTH + wi * CELL_STEP
            y = MONTH_LABEL_HEIGHT + di * CELL_STEP
            level = entry.get("level", 0)
            color = colors[min(level, len(colors) - 1)]
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'rx="2" ry="2" fill="{color}"><title>{entry["date"]}</title></rect>'
            )

    parts.append("</svg>")
    return "\n".join(parts)
