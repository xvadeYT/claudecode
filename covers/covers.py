"""Render ADM reel cover options (1080x1920) with Playwright.

Built on the crowned-figure logo (logo.png, 2000x2000, background #111111).
Everything important sits inside the middle 1080x1440, because the Instagram
profile grid crops reel covers to 3:4 from the center.

    python3 covers/covers.py            # render the options
    python3 covers/covers.py C 1 1000   # render final/cover_0001.jpg..cover_1000.jpg for option C
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts.css")).read().replace("url(fonts/", "url(file://" + HERE + "/fonts/")
LOGO = "file://" + os.path.join(HERE, "logo.png")

BG = "#111111"
BASE = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{BG}}}
body{{position:relative}}
.stage{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
/* the logo's own ground is #111; fade its edges and the cut-off shoulders into the page */
.logo{{display:block;-webkit-mask-image:linear-gradient(to bottom,#000 0%,#000 62%,transparent 94%),radial-gradient(circle at 50% 45%,#000 55%,transparent 72%);
  -webkit-mask-composite:source-in;mask-composite:intersect}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse 75% 55% at 50% 46%,transparent 40%,rgba(0,0,0,.72) 100%);pointer-events:none}}
.grain{{position:absolute;inset:0;opacity:.09;mix-blend-mode:screen;pointer-events:none}}
.lab{{font-family:'JetBrains Mono';font-weight:500;color:#5E5E5E;letter-spacing:.55em;text-transform:uppercase;padding-left:.55em}}
"""
GRAIN = """<svg class="grain" width="1080" height="1920"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""

# Plain silhouette traced from the logo's geometry (2000x2000 space), no pattern.
def silhouette(width, fill="url(#g)", glow=False):
    g = ("""<radialGradient id="glow" cx="50%" cy="46%" r="42%"><stop offset="0" stop-color="#9a9a9a" stop-opacity=".22"/><stop offset="1" stop-color="#9a9a9a" stop-opacity="0"/></radialGradient>"""
         if glow else "")
    halo = '<rect x="0" y="0" width="2000" height="2000" fill="url(#glow)"/>' if glow else ""
    return f"""<svg width="{width}" height="{width}" viewBox="0 0 2000 2000">
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="220" x2="0" y2="1960"><stop offset="0" stop-color="#7A7A7A"/><stop offset=".55" stop-color="#5C5C5C"/><stop offset=".78" stop-color="#2E2E2E"/><stop offset="1" stop-color="#0E0E0E"/></linearGradient>{g}</defs>
{halo}
<g fill="{fill}">
  <circle cx="692" cy="311" r="31"/><circle cx="967" cy="240" r="33"/><circle cx="1241" cy="311" r="31"/>
  <polygon points="690,338 842,432 967,262 1092,432 1244,338 1246,480 688,480"/>
  <rect x="685" y="497" width="566" height="68" rx="8"/>
  <circle cx="967" cy="976" r="351"/>
  <ellipse cx="967" cy="2010" rx="642" ry="615"/>
</g></svg>"""

def logo(width):
    return f'<img class="logo" src="{LOGO}" width="{width}" height="{width}">'

def opt_a(n):  # Logo only
    return f'<div class="stage">{logo(1000)}</div>'

def opt_b(n):  # Logo + ADM
    return f"""<div class="stage" style="gap:10px">{logo(900)}<div class="lab" style="font-size:46px;color:#6A6A6A;margin-top:-30px">ADM</div></div>"""

def opt_c(n):  # Numbered
    return f"""<div class="stage">{logo(640)}
<div style="font-family:Anton;font-size:250px;line-height:1;color:#8A8A8A;letter-spacing:.06em;margin-top:0">{n:04d}</div>
<div class="lab" style="font-size:27px;letter-spacing:.42em;padding-left:.42em;color:#6A6A6A;margin-top:34px">i will become a millionaire</div></div>"""

def opt_d(n):  # Plain silhouette, nothing else
    return f'<div class="stage">{silhouette(1000)}</div>'

def opt_e(n):  # Fog: dim silhouette with a faint halo, one quiet line
    return f"""<div class="stage">{silhouette(940, fill="url(#g)", glow=True)}
<div class="lab" style="font-size:30px;color:#606060;margin-top:10px">follow the journey</div></div>"""

OPTIONS = {"A_logo": opt_a, "B_logo_adm": opt_b, "C_numbered": opt_c, "D_plain": opt_d, "E_fog": opt_e}

def page(body):
    return f"<!doctype html><html><head><meta charset=utf8><style>{FONTS}{BASE}</style></head><body>{body}<div class=vig></div>{GRAIN}</body></html>"

async def render(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME") or None) if os.environ.get("CHROME") is not None else await p.chromium.launch(executable_path="/opt/pw-browsers/chromium") if os.path.exists("/opt/pw-browsers/chromium") else await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        tmp = os.path.join(HERE, "_tmp.html")
        for path, body in jobs:
            open(tmp, "w").write(page(body))
            await pg.goto("file://" + tmp)
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=path, **({"type": "jpeg", "quality": 88} if path.endswith(".jpg") else {}))
        os.remove(tmp)
        await b.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        key = next(k for k in OPTIONS if k.startswith(sys.argv[1].upper()))
        out = os.path.join(HERE, "final")
        os.makedirs(out, exist_ok=True)
        jobs = [(os.path.join(out, f"cover_{n:04d}.jpg"), OPTIONS[key](n)) for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1)]
    else:
        os.makedirs(os.path.join(HERE, "options"), exist_ok=True)
        jobs = [(os.path.join(HERE, "options", f"{k}.png"), f(1)) for k, f in OPTIONS.items()]
    asyncio.run(render(jobs))
    print("rendered", len(jobs))
