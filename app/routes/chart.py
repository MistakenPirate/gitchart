import re

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse, Response

from app.services.colors import generate_palette, get_theme
from app.services.github import fetch_contributions
from app.services.svg import generate_svg

router = APIRouter()

CACHE_TTL = 86400  # 24 hours
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def svg_response(svg: str) -> Response:
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": f"public, max-age={CACHE_TTL}"},
    )


def resolve_palette(color_or_theme: str | None) -> tuple[list[str] | None, bool]:
    """Returns (palette, was_valid). was_valid is False only when a color was provided but unrecognized."""
    if color_or_theme is None:
        return None, True
    theme = get_theme(color_or_theme)
    if theme:
        return theme, True
    if re.fullmatch(r"[0-9a-fA-F]{6}", color_or_theme):
        return generate_palette(color_or_theme), True
    return None, False


@router.get("/{username}")
async def chart(
    username: str,
    color: str | None = Query(None, description="6-digit hex color or theme name (blue, purple, orange, red, pink, halloween)"),
    start: str | None = Query(None, alias="from", description="Start date (YYYY-MM-DD)"),
    to: str | None = Query(None, description="End date (YYYY-MM-DD)"),
):
    if start and not DATE_PATTERN.match(start):
        return PlainTextResponse("Invalid 'from' date. Use YYYY-MM-DD", status_code=400)
    if to and not DATE_PATTERN.match(to):
        return PlainTextResponse("Invalid 'to' date. Use YYYY-MM-DD", status_code=400)
    palette, valid = resolve_palette(color)
    if not valid:
        return PlainTextResponse("Invalid color. Use 6-digit hex or theme name (blue, purple, orange, red, pink, halloween)", status_code=400)
    contributions = await fetch_contributions(username, from_date=start, to_date=to)
    if not contributions:
        return PlainTextResponse("User not found or no contributions", status_code=404)
    return svg_response(generate_svg(contributions, palette) if palette else generate_svg(contributions))
