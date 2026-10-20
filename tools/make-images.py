# Regenerates og.png (social share image) from assets/nuvera-logo-hd-1024.png. Run from the repo root.
import base64
from playwright.sync_api import sync_playwright
logo = base64.b64encode(open('assets/nuvera-logo-hd-1024.png','rb').read()).decode()
og=f'''<html><body style="margin:0;width:1200px;height:630px;background:#F7F0E3;font-family:Poppins,sans-serif;color:#3A2816;position:relative;overflow:hidden">
<img src="data:image/png;base64,{logo}" style="position:absolute;right:70px;top:75px;width:480px;height:480px;filter:drop-shadow(0 18px 40px rgba(150,105,40,.35))">
<div style="position:absolute;left:80px;top:90px;font-size:28px;font-weight:600;letter-spacing:.5px">Nuvera Form</div>
<div style="position:absolute;left:80px;top:170px;width:560px;font-size:64px;font-weight:700;line-height:1.1">Research peptides for qualified laboratories.</div>
<div style="position:absolute;left:80px;top:520px;font-size:24px">nuveraform.com · Research use only · 21+</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':630})
    pg.set_content(og);pg.wait_for_timeout(300);pg.screenshot(path='og.png');b.close()
