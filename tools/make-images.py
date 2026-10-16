from playwright.sync_api import sync_playwright
og='''<html><body style="margin:0;width:1200px;height:630px;background:#F7F0E3;font-family:Poppins;color:#3A2816;position:relative;overflow:hidden">
<svg style="position:absolute;right:40px;top:90px" width="440" height="440" viewBox="0 0 400 340"><path d="M70 60L150 110L250 80L320 170L260 250L330 300" stroke="#BF943C" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="70" cy="60" r="34" fill="#DEB25A"/><circle cx="150" cy="110" r="42" fill="#BF943C"/><circle cx="250" cy="80" r="40" fill="#B87A6C"/><circle cx="320" cy="170" r="48" fill="#DEB25A"/><circle cx="260" cy="250" r="38" fill="#BF943C"/><circle cx="330" cy="300" r="34" fill="#B87A6C"/></svg>
<div style="position:absolute;left:80px;top:90px;font-size:28px;font-weight:600;display:flex;align-items:center;gap:14px"><span style="width:18px;height:18px;border-radius:50%;background:#BF943C"></span>Nuvera Form</div>
<div style="position:absolute;left:80px;top:180px;width:650px;font-size:68px;font-weight:700;line-height:1.1">Research peptides for qualified laboratories.</div>
<div style="position:absolute;left:80px;top:520px;font-size:26px">nuveraform.com · Research use only · 21+</div></body></html>'''
ic='''<html><body style="margin:0;width:180px;height:180px;background:#BF943C"><svg width="180" height="180" viewBox="0 0 32 32"><circle cx="11" cy="20" r="4.5" fill="#F7F0E3"/><circle cx="21" cy="11" r="3.2" fill="#B87A6C"/></svg></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':630})
    pg.set_content(og);pg.screenshot(path='og.png')
    pg.set_viewport_size({'width':180,'height':180});pg.set_content(ic);pg.screenshot(path='apple-touch-icon.png');b.close()
