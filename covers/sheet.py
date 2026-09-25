import asyncio, os, glob
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
files=sorted(glob.glob(os.path.join(HERE,'options','[A-Z]_*.png')))
cells=''.join(f"""<figure><div class="f"><img src="file://{p}"><i></i></div><figcaption>{os.path.basename(p)[0]} · {os.path.basename(p)[2:-4]}</figcaption></figure>""" for p in files)
html=f"""<!doctype html><html><head><meta charset=utf8><style>{open(os.path.join(HERE,'fonts.css')).read().replace('url(fonts/','url(file://'+HERE+'/fonts/')}
body{{margin:0;background:#1a1a18;padding:40px;display:flex;gap:30px;width:max-content}}
figure{{margin:0}} .f{{position:relative;width:360px;height:640px}} img{{width:360px;height:640px;display:block}}
i{{position:absolute;left:0;right:0;top:80px;bottom:80px;border:2px dashed rgba(255,255,255,.35)}}
figcaption{{font-family:'JetBrains Mono';font-weight:700;font-size:26px;color:#eee;margin-top:16px;text-transform:uppercase;letter-spacing:2px}}
</style></head><body>{cells}</body></html>"""
open(os.path.join(HERE,'_sheet.html'),'w').write(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get("CHROME","/opt/pw-browsers/chromium"))
        pg=await b.new_page(viewport={'width':1980,'height':800})
        await pg.goto('file://'+os.path.join(HERE,'_sheet.html')); await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=os.path.join(HERE,'options','_ALL_OPTIONS.png'),full_page=True)
        await b.close()
    os.remove(os.path.join(HERE,'_sheet.html'))
asyncio.run(main())
