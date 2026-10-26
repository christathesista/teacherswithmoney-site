# Speakers for the Summit page

`speakers.json` is a list. Each speaker is an object:

```json
{
  "name": "Davy Yap",
  "photo": "assets/speakers/davy-yap.jpg",
  "title": "Middle school teacher, millionaire on a teacher paycheck",
  "session": "The retirement accounts most teachers were never told about",
  "day": 1
}
```

Drop the photo in `assets/speakers/` (square, at least 600 by 600). Then run `python3 build.py`. An empty list shows "The lineup is coming together right now."
