"""M4 QA: links, form, accessibility (axe-core), performance, responsive screenshots.

    npm install axe-core@4 && pip install playwright && playwright install chromium
    python3 -m http.server 8765 &        # from the repository root
    python3 tools/qa.py                  # or: python3 tools/qa.py links a11y
Results: qa-out/report.json and screenshots in qa-out/.
"""
import asyncio, json, os, re, sys
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright

BASE = 'http://localhost:8765/'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PAGES = ['index.html', 'journey.html', 'person.html', 'motion.html', 'partnerships.html']
WIDTHS = [(360, 780), (390, 844), (768, 1024), (1024, 768), (1440, 900), (1920, 1080)]
AXE = open(os.environ.get('AXE_JS', 'node_modules/axe-core/axe.min.js')).read()
OUT = os.environ.get('QA_OUT', 'qa-out')
os.makedirs(OUT, exist_ok=True)
report = {}


async def skip_intro(pg):
    if await pg.evaluate("document.documentElement.classList.contains('intro-on')"):
        await pg.click('#intro-skip')
    await pg.wait_for_timeout(300)


async def links(b):
    """Every href/src on every page resolves; every #anchor exists on its target page."""
    ctx = await b.new_context(); pg = await ctx.new_page()
    ids, refs = {}, []
    for p in PAGES:
        await pg.goto(BASE + p)
        ids[p] = await pg.evaluate("[...document.querySelectorAll('[id]')].map(e=>e.id)")
        found = await pg.evaluate("""[...document.querySelectorAll('a[href],img[src],source[srcset],video[data-src],video[poster],link[href],script[src]')]
            .flatMap(e=>{const out=[];if(e.getAttribute('href'))out.push(e.getAttribute('href'));if(e.getAttribute('src'))out.push(e.getAttribute('src'));
            if(e.dataset&&e.dataset.src)out.push(e.dataset.src);if(e.getAttribute('poster'))out.push(e.getAttribute('poster'));if(e.dataset&&e.dataset.preview)out.push(e.dataset.preview);
            if(e.getAttribute('srcset'))e.getAttribute('srcset').split(',').forEach(s=>out.push(s.trim().split(' ')[0]));return out})""")
        refs += [(p, r) for r in found]
    bad, external = [], set()
    for page, r in refs:
        if r.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            if not r.startswith(BASE): external.add(r)
            continue
        path, _, frag = r.partition('#')
        target = path or page
        if path and not os.path.exists(REPO + path):
            bad.append(f'{page} → {r} (fichier absent)')
        if frag and frag not in ids.get(target, []):
            bad.append(f'{page} → {r} (ancre absente)')
    await ctx.close()
    report['links'] = {'checked': len(refs), 'broken': bad, 'external': sorted(external)}


async def form(b):
    ctx = await b.new_context(viewport={'width': 1440, 'height': 900}); pg = await ctx.new_page()
    await pg.goto(BASE + 'partnerships.html#contact'); await pg.wait_for_timeout(400)
    await pg.click('.pt-form button[type=submit]'); await pg.wait_for_timeout(200)
    empty = await pg.evaluate("({status:document.querySelector('.form-status').textContent,invalid:document.querySelectorAll('[aria-invalid=true]').length,focus:document.activeElement.id})")
    await pg.screenshot(path=f'{OUT}/form_errors.png')
    await pg.fill('#nom', 'Test'); await pg.fill('#organisation', 'Marque'); await pg.fill('#email', 'pas-un-email')
    await pg.select_option('#projet', index=1); await pg.fill('#message', 'Bonjour')
    await pg.click('.pt-form button[type=submit]'); await pg.wait_for_timeout(200)
    bad_email = await pg.evaluate("({status:document.querySelector('.form-status').textContent,err:document.getElementById('email-err').textContent,focus:document.activeElement.id})")
    await pg.fill('#email', 'test@exemple.com')
    reqs = []
    pg.on('request', lambda r: reqs.append(r.url) if r.method == 'POST' else None)
    await pg.click('.pt-form button[type=submit]'); await pg.wait_for_timeout(300)
    ok = await pg.evaluate("document.querySelector('.form-status').textContent")
    await pg.screenshot(path=f'{OUT}/form_ok.png')
    report['form'] = {'empty_submit': empty, 'bad_email': bad_email, 'valid_submit': ok, 'network_posts': reqs,
                      'kit_button_disabled': await pg.evaluate("document.querySelector('.kit button').disabled")}
    await ctx.close()


async def a11y(b):
    res = {}
    for w, h, tag in [(1440, 900, 'desktop'), (390, 844, 'mobile')]:
        ctx = await b.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce'); pg = await ctx.new_page()
        for p in PAGES:
            await pg.goto(BASE + p); await skip_intro(pg)
            # make every reveal visible so axe measures final contrast
            await pg.evaluate("document.querySelectorAll('.reveal,.fade,.fig').forEach(n=>n.classList.add('in'))")
            await pg.add_script_tag(content=AXE)
            r = await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})")
            res[f'{tag}:{p}'] = [{'id': v['id'], 'impact': v['impact'], 'help': v['help'], 'n': len(v['nodes']),
                                  'targets': [n['target'] for n in v['nodes'][:4]]} for v in r['violations']]
        await ctx.close()
    report['axe'] = res


async def keyboard(b):
    ctx = await b.new_context(viewport={'width': 1440, 'height': 900}); pg = await ctx.new_page()
    await pg.goto(BASE + 'index.html'); await skip_intro(pg)
    seq = []
    for _ in range(8):
        await pg.keyboard.press('Tab')
        seq.append(await pg.evaluate("(()=>{const e=document.activeElement;return (e.textContent||e.getAttribute('aria-label')||e.tagName).trim().slice(0,30)})()"))
    outline = await pg.evaluate("getComputedStyle(document.activeElement).outlineStyle")
    await pg.keyboard.press('Escape')
    report['keyboard'] = {'tab_order_home': seq, 'focus_outline': outline}
    await ctx.close()


async def perf(b):
    res = {}
    for w, h, tag in [(1440, 900, 'desktop'), (390, 844, 'mobile')]:
        for p in PAGES:
            ctx = await b.new_context(viewport={'width': w, 'height': h}); pg = await ctx.new_page()
            await pg.add_init_script("""
              window.__lcp=0;window.__cls=0;
              new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
              new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});""")
            # skip the intro so we measure the page itself
            await pg.add_init_script("try{localStorage.setItem('elanga:intro-v2','1')}catch(e){}")
            await pg.goto(BASE + p, wait_until='load'); await pg.wait_for_timeout(1500)
            m = await pg.evaluate("""(()=>{const r=performance.getEntriesByType('resource');const nav=performance.getEntriesByType('navigation')[0];
              const sum=f=>r.filter(f).reduce((a,e)=>a+(e.encodedBodySize||e.transferSize||0),0);
              return {lcp_ms:Math.round(window.__lcp),cls:+window.__cls.toFixed(3),requests:r.length+1,
                      kb_total:Math.round((sum(()=>true)+(nav.encodedBodySize||0))/1024),
                      kb_img:Math.round(sum(e=>/\\.(jpg|webp|png|svg)/.test(e.name))/1024),
                      kb_video:Math.round(sum(e=>/\\.mp4/.test(e.name))/1024),
                      kb_font:Math.round(sum(e=>/\\.woff2/.test(e.name))/1024),
                      dom_ready_ms:Math.round(nav.domContentLoadedEventEnd)}})()""")
            res[f'{tag}:{p}'] = m
            await ctx.close()
    report['perf'] = res


async def shots(b):
    errs = []
    for p in PAGES:
        for w, h in WIDTHS:
            ctx = await b.new_context(viewport={'width': w, 'height': h}); pg = await ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(f'{p} {w}: {e}'))
            pg.on('console', lambda m: errs.append(f'{p} {w}: {m.text}') if m.type == 'error' else None)
            await pg.add_init_script("try{localStorage.setItem('elanga:intro-v2','1')}catch(e){}")
            await pg.goto(BASE + p); await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'{OUT}/{p[:-5]}_{w}.png')
            over = await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
            if over: errs.append(f'{p} {w}: débordement horizontal ({await pg.evaluate("document.documentElement.scrollWidth")}px)')
            await ctx.close()
    report['responsive'] = {'shots': len(PAGES) * len(WIDTHS), 'issues': errs}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for step in sys.argv[1:] or ['links', 'form', 'a11y', 'keyboard', 'perf', 'shots']:
            await globals()[step](b)
        await b.close()
    json.dump(report, open(f'{OUT}/report.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1)[:6000])

asyncio.run(main())
