# ADM: 1000 reels

Start here. This is everything for the 1000-reel run, two posts a day for 500 days.

## What's in each folder

| Folder | What's inside | Do you need to open it? |
|---|---|---|
| `QUOTES/` | `QUOTES_GENZ_V4.txt`: the 1000 quotes, one per line (line 1 = reel_0001).<br>`SCHEDULE_V4.csv`: every reel with its date, time, caption and hashtags. | Only to render the videos. |
| `COVERS/` | `cover_0001.jpg` … `cover_1000.jpg`. One cover per reel, same number. | Yes. Put these on your phone. |
| `BLOTTER/` | The page behind your Reel Blotter link. | No. Just use the link below. |
| `BRAND/` | `logo.png`, your crowned logo, and `cover-options.png`, the 5 cover designs we picked from. | Only if you need the logo. |
| `_WORKSHOP/` | The scripts and source files that make everything above. | No. Leave it alone. |

**Reel Blotter:** https://claude.ai/artifact/WASzn8qN4Ypa1XRRybXcqg

## How your PC is organized

```
Downloads\ADM\
  1_BACKGROUNDS\   your raw background clips (never delete these)
  2_REELS\         reel_0001.mp4 … reel_1000.mp4, the videos you post
  3_COVERS\        cover_0001.jpg … cover_1000.jpg
  4_QUOTES\        QUOTES_GENZ_V4.txt, SCHEDULE_V4.csv
  5_TOOLS\         the render scripts
  _OLD\            old versions (V2, V3, the short quotes). Delete when you're sure you don't need them.
```

## Posting (2 a day)

1. Open the Reel Blotter. The box at the top shows the next reel, its cover, and the time to post.
2. In Instagram, make a Reel with that video, add music, then **Edit cover → Add from camera roll** and pick the cover with the same number.
3. In the blotter, tap **Copy caption** and paste it into Instagram.
4. **More options → Schedule** for the date and time the blotter shows.
5. Tap **Mark posted** in the blotter. Instagram schedules up to 75 days ahead, so do a few weeks at a time.

Recommended times: weekdays **12:00 PM & 7:00 PM**, weekends **11:00 AM & 8:00 PM**. After two weeks, check Instagram's "Most active times" and change them in the blotter.

## Rebuilding (only if you change something)

- Edited quotes in `_WORKSHOP/quotes/`? Run `python3 _WORKSHOP/build_reels.py`.
- Changed the cover design? Run `python3 _WORKSHOP/make_covers.py C 1 1000`.
