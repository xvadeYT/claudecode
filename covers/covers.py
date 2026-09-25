"""Render reel cover options (1080x1920) with Playwright.

Everything important sits inside the middle 1080x1440, because the Instagram
profile grid crops reel covers to 3:4 from the center.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts.css")).read()

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden}
body{display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative}
"""

MARK = """<svg width="{s}" height="{s}" viewBox="-300 -300 600 600" fill="none">
  <circle cx="0" cy="0" r="270" stroke="{c}" stroke-width="{w}"/>
  <polyline points="-165,125 0,-150 165,125" stroke="{c}" stroke-width="{w2}" stroke-linejoin="miter" stroke-linecap="square"/>
  <line x1="-78" y1="30" x2="78" y2="30" stroke="{c}" stroke-width="{w}"/>
  <circle cx="0" cy="-205" r="{d}" fill="{c}"/>
</svg>"""

def mark(size, color, w=10, w2=22, dot=16):
    return MARK.format(s=size, c=color, w=w, w2=w2, d=dot)

def opt_a(n):  # Monogram
    return f"""<style>body{{background:#0B0B0A;color:#F2EEE6}}
.adm{{font-family:Anton;font-size:420px;line-height:.9;letter-spacing:6px}}
.rule{{width:260px;height:4px;background:#C9A45C;margin:48px 0 40px}}
.sub{{font-family:'JetBrains Mono';font-weight:700;font-size:40px;letter-spacing:14px;color:#C9A45C}}
</style><div class="adm">ADM</div><div class="rule"></div><div class="sub">FOLLOW THE JOURNEY</div>"""

def opt_b(n):  # Symbol only
    return f"""<style>body{{background:#0B0B0A}}</style>{mark(620, '#C9A45C')}"""

def opt_c(n):  # Numbered series
    return f"""<style>body{{background:#0B0B0A;color:#F2EEE6}}
.top{{font-family:'JetBrains Mono';font-weight:700;font-size:44px;letter-spacing:16px;color:#C9A45C;margin-bottom:30px;display:flex;align-items:center;gap:26px}}
.num{{font-family:Anton;font-size:400px;line-height:1;letter-spacing:4px}}
.of{{font-family:'JetBrains Mono';font-weight:500;font-size:40px;letter-spacing:10px;color:#8A857B;margin-top:26px}}
</style><div class="top">{mark(70,'#C9A45C',w=18,w2=36,dot=26)}ADM</div><div class="num">{n:04d}</div><div class="of">OF 1000 · FOLLOW THE JOURNEY</div>"""

def opt_d(n):  # Signature
    return f"""<style>body{{background:#10120F;color:#EFE6D2}}
.name{{font-family:'Cormorant Garamond';font-weight:600;font-size:118px;letter-spacing:8px;line-height:1;white-space:nowrap}}
.it{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:96px;color:#C9A45C;margin-top:34px}}
.sm{{position:absolute;top:360px}}
</style><div class="sm">{mark(150,'#C9A45C',w=12,w2=24,dot=18)}</div><div class="name">ADAM SCALEZ</div><div class="it">follow the journey</div>"""

def opt_e(n):  # Light / inverse
    return f"""<style>body{{background:#F2EEE6;color:#0B0B0A}}
.adm{{font-family:'Archivo Black';font-size:330px;line-height:1;letter-spacing:-6px}}
.adm span{{color:#B8322A}}
.sub{{font-family:'JetBrains Mono';font-weight:700;font-size:38px;letter-spacing:12px;margin-top:40px}}
</style><div class="adm">ADM<span>.</span></div><div class="sub">FOLLOW THE JOURNEY</div>"""

OPTIONS = {"A_monogram": opt_a, "B_symbol": opt_b, "C_numbered": opt_c, "D_signature": opt_d, "E_light": opt_e}

async def render(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/opt/pw-browsers/chromium"))
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for path, body in jobs:
            html = f"<!doctype html><html><head><meta charset=utf8><style>{FONTS}{BASE}</style></head><body>{body}</body></html>"
            tmp = os.path.join(HERE, "_tmp.html")
            open(tmp, "w").write(html)
            await pg.goto("file://" + tmp)
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=path)
        os.remove(tmp)
        await b.close()

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "options"), exist_ok=True)
    jobs = [(os.path.join(HERE, "options", f"{k}.png"), f(1)) for k, f in OPTIONS.items()]
    asyncio.run(render(jobs))
    print("rendered", len(jobs))
