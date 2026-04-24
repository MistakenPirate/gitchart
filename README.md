# GitChart

Drop in a GitHub username, get back an SVG of their contribution graph.

```
/{username}
/{username}?color=blue
/{username}?color=409ba5
/{username}?from=2025-01-01&to=2025-06-30
```

Stick it in a README:

```markdown
![contributions](https://your-domain.com/torvalds)
```

## Colors

Themes: `green` (default), `blue`, `purple`, `orange`, `red`, `pink`, `halloween`

Or pass any hex color: `?color=409ba5`

## Running it

```bash
uv run uvicorn main:app --reload
```
