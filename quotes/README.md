# Gen Z reels, V4

1000 new quotes written in the same style as the first 100 in `REELS_V3`: full sentences that make a point and finish with a twist, 8–19 words each (11 on average). They're set up to post two a day for 500 days.

| File | What it is |
|---|---|
| `QUOTES_GENZ_V4.txt` | One quote per line, already in posting order. Line 1 = `reel_0001.mp4`. Point the renderer at this file. |
| `SCHEDULE_V4.csv` | Every reel with its day, date, post time, caption, call to action and hashtags. |
| `reel-blotter.html` | Source of the Reel Blotter 1000 artifact. |
| `src/batchNN.txt` | The quotes by theme, one per line as `caption title|on-screen quote`. |
| `build.py` | Rebuilds the three outputs from `src/`. Run `python3 quotes/build.py`. |

Themes (100 each): family, being young / school, discipline, money, doubters & circle, future / vision, Gen Z & online, faith, love / gym / comebacks / trading, time & self-belief. The build deals them out in rotation, so two reels in a row never come from the same theme.

## Posting times (recommended defaults, your local time)

| | Post 1 | Post 2 |
|---|---|---|
| Mon–Fri | 12:00 PM | 7:00 PM |
| Sat–Sun | 11:00 AM | 8:00 PM |

Midday catches the lunch scroll, and the evening post goes out just before the 8–10 PM peak. After two weeks, open Professional dashboard → Total followers → Most active times and move the times to match your own followers. You can change them in the blotter and every date updates. Posting at the right time only gets a reel seen at the start. What gets it pushed further is the first 3 seconds, watch time, and how many people send it or save it. That's why every caption ends with a line asking people to send it or save it.
