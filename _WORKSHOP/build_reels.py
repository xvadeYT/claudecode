"""Build the V4 reel library: posting order, render file, schedule CSV and the Reel Blotter page.

Sources are _WORKSHOP/quotes/batchNN.txt, one reel per line as `caption title|on-screen quote`.
Each batch is one theme, so the posting order deals them out round-robin: two reels
in a row never come from the same theme.

    python3 _WORKSHOP/build_reels.py
"""
import csv
import datetime as dt
import glob
import json
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "quotes")
OUT_QUOTES = os.path.join(ROOT, "QUOTES", "QUOTES_GENZ_V4.txt")
OUT_CSV = os.path.join(ROOT, "QUOTES", "SCHEDULE_V4.csv")
OUT_HTML = os.path.join(ROOT, "BLOTTER", "reel-blotter.html")

START = dt.date(2026, 9, 26)
# Recommended defaults, local time. Slot 1 = midday scroll, slot 2 = just before the evening peak.
TIMES = {"weekday": ("12:00", "19:00"), "weekend": ("11:00", "20:00")}

# Keep in sync with TAGSETS / CTAS in quotes/blotter_template.html.
TAGSETS = [
    "#relatable #motivation #motivationalquotes #successmindset #explorepage",
    "#relatable #motivation #selfimprovement #discipline #reels",
    "#relatable #motivation #personalgrowth #mindset #reelsinstagram",
    "#relatable #motivation #motivationalquotes #hustle #viralvideo",
    "#relatable #motivation #inspiration #successmindset #explorepage",
    "#relatable #motivation #selfimprovement #grind #reels",
]
CTAS = [
    "send this to someone who needs it today.",
    "save this for the days you want to quit.",
    "send this to the one who's building with you.",
    "follow for 2 a day. no days off.",
    "save this. read it again in a year.",
    'comment "locked in" if this is you.',
]


def load_batches():
    batches = []
    for path in sorted(glob.glob(os.path.join(SRC, "batch*.txt"))):
        rows = []
        for i, line in enumerate(open(path, encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("|")
            assert len(parts) == 2, f"{path}:{i} needs exactly one |"
            rows.append((parts[0].strip(), parts[1].strip()))
        batches.append(rows)
    return batches


def validate(rows):
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
    assert len(rows) == 1000, f"expected 1000 reels, got {len(rows)}"
    assert len({norm(q) for _, q in rows}) == len(rows), "duplicate quote"
    assert len({t for t, _ in rows}) == len(rows), "duplicate caption title"
    for t, q in rows:
        assert re.fullmatch(r"[\x20-\x7e]+", t + q), f"non-ASCII character in: {q}"
        assert len(q.split()) >= 8, f"too short: {q}"
        assert len(q) <= 95, f"too long for the frame: {q}"


def posting_order(batches):
    rng = random.Random(2026)
    decks = [rng.sample(b, len(b)) for b in batches]
    order = []
    rnd = 0
    while any(decks):
        # Rotate which theme leads each round so the same pair never repeats back to back.
        idx = list(range(len(decks)))
        idx = idx[rnd % len(idx):] + idx[: rnd % len(idx)]
        for j in idx:
            if decks[j]:
                order.append(decks[j].pop())
        rnd += 1
    return order


def main():
    rows = posting_order(load_batches())
    validate(rows)

    with open(OUT_QUOTES, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(q for _, q in rows) + "\n")

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reel", "file", "day", "date", "weekday", "post", "time", "caption_title", "on_screen_quote", "cta", "hashtags"])
        for i, (title, quote) in enumerate(rows):
            n = i + 1
            day = (n + 1) // 2
            slot = 1 if n % 2 else 2
            date = START + dt.timedelta(days=day - 1)
            kind = "weekend" if date.weekday() >= 5 else "weekday"
            w.writerow([n, f"reel_{n:04d}.mp4", day, date.isoformat(), date.strftime("%a"), slot,
                        TIMES[kind][slot - 1], title, quote, CTAS[i % len(CTAS)], TAGSETS[i % len(TAGSETS)]])

    data = json.dumps([[t, q] for t, q in rows], ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
    tpl = open(os.path.join(SRC, "blotter_template.html"), encoding="utf-8").read()
    assert tpl.count("__DATA__") == 1
    open(OUT_HTML, "w", encoding="utf-8").write(tpl.replace("__DATA__", data))

    words = [len(q.split()) for _, q in rows]
    print(f"{len(rows)} reels, avg {sum(words) / len(words):.1f} words, "
          f"days 1-{(len(rows) + 1) // 2} ({START} to {START + dt.timedelta(days=(len(rows) + 1) // 2 - 1)})")


if __name__ == "__main__":
    main()
