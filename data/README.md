# Summit speakers

`speakers.json` feeds the lineup on /summit/, rendered as an album tracklist (Side A = Day 1, Side B = Day 2).
An empty list `[]` shows the "tracklist drops in January" state with blank tracks.

Each entry:

```json
{
  "name": "Full Name",
  "photo": "assets/speakers/full-name.jpg",
  "title": "What they do, one line",
  "session": "Session title",
  "day": 1,
  "side": "A",
  "bio": "Two or three sentences for the liner notes.",
  "links": [{ "label": "Website", "url": "https://..." }, { "label": "Instagram", "url": "https://..." }]
}
```

- `side` is "A" (Day 1, Saturday) or "B" (Day 2, Sunday). If it's missing, `day` decides (2 = B, anything else = A).
- Photos go in `assets/speakers/`, square, at least 600 by 600.
- Tracks are numbered in the order they appear in the file, per side.
- After editing: `python3 build.py`, then commit and push.
