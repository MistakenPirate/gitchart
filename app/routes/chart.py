import re

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse, Response

from app.services.colors import generate_palette, get_theme
from app.services.github import fetch_contributions
from app.services.svg import generate_svg

router = APIRouter()

CACHE_TTL = 86400  # 24 hours


def svg_response(svg: str) -> Response:
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": f"public, max-age={CACHE_TTL}"},
    )


def resolve_palette(color_or_theme: str | None) -> list[str] | None:
    if color_or_theme is None:
        return None
    theme = get_theme(color_or_theme)
    if theme:
        return theme
    if re.fullmatch(r"[0-9a-fA-F]{6}", color_or_theme):
        return generate_palette(color_or_theme)
    return None


@router.get("/{username}")
async def chart(
    username: str,
    color: str | None = Query(None, description="6-digit hex color or theme name (blue, purple, orange, red, pink, halloween)"),
    start: str | None = Query(None, alias="from", description="Start date (YYYY-MM-DD)"),
    to: str | None = Query(None, description="End date (YYYY-MM-DD)"),
):
    contributions = await fetch_contributions(username, from_date=start, to_date=to)
    if not contributions:
        return PlainTextResponse("User not found or no contributions", status_code=404)
    palette = resolve_palette(color)
    return svg_response(generate_svg(contributions, palette) if palette else generate_svg(contributions))
