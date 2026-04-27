# GitChart

Drop in a GitHub username, get back an SVG of their contribution graph.

```
/{username}
/{username}?color=blue
/{username}?color=409ba5
/{username}?from=2025-06-01&to=2026-04-20
```

Stick it in a README:

```markdown
![contributions](https://your-domain.com/torvalds)
```

## Examples

### Default (green)
`/mistakenpirate`

![default](examples/default.svg)

### Blue theme
`/mistakenpirate?color=blue`

![blue](examples/blue.svg)

### Purple theme
`/mistakenpirate?color=purple`

![purple](examples/purple.svg)

### Orange theme
`/mistakenpirate?color=orange`

![orange](examples/orange.svg)

### Red theme
`/mistakenpirate?color=red`

![red](examples/red.svg)

### Pink theme
`/mistakenpirate?color=pink`

![pink](examples/pink.svg)

### Halloween theme
`/mistakenpirate?color=halloween`

![halloween](examples/halloween.svg)

### Custom hex color
`/mistakenpirate?color=409ba5`

![custom-hex](examples/custom-hex.svg)

### Date range (from & to)
`/mistakenpirate?from=2025-06-01&to=2026-04-20`

![date-range](examples/date-range.svg)

### From date only
`/mistakenpirate?from=2025-06-01`

![from-only](examples/from-only.svg)

### To date only
`/mistakenpirate?to=2026-04-20`

![to-only](examples/to-only.svg)

## Colors

Themes: `green` (default), `blue`, `purple`, `orange`, `red`, `pink`, `halloween`

Or pass any hex color: `?color=409ba5`

## Running it

```bash
uv run uvicorn main:app --reload
```
