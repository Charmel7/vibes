from playwright.sync_api import sync_playwright
import os
os.chdir('/home/claude/vibes/doc')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto('file:///home/claude/vibes/doc/doc.html'); pg.wait_for_timeout(800)
    # overflow report
    print(pg.evaluate("""()=>[...document.querySelectorAll('.page')].map((p,i)=>{const r=p.getBoundingClientRect();let m=0;p.querySelectorAll('*').forEach(e=>{const b=e.getBoundingClientRect();if(b.height&&!e.closest('.dot')&&e.className!='ft'&&b.bottom-r.top>m)m=b.bottom-r.top});return [i+1,Math.round(m),Math.round(r.height)]})"""))
    pg.pdf(path='VIBES-YTH-Live-2026-Application.pdf',prefer_css_page_size=True,print_background=True)
    b.close()
