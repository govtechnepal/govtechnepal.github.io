#!/usr/bin/env python3
"""Static site generator for govtechnepal.org (Python 3, no dependencies).
Run:  python3 src/build.py   -> writes HTML, sitemap.xml and robots.txt into the site root."""
import json, os, html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE='https://govtechnepal.org'
GITHUB='https://github.com/nirajbhusal/GovTech'
LIPI_WIN='https://drive.google.com/file/d/1DGU8rzzZxqs1QX37jr98SKRLUNS8aqdH/view?usp=drivesdk'
LIPI_MAC='/downloads/lipi/Lipi-macOS-0.1.6.dmg'
LIPI_CHROME='/downloads/lipi/Lipi-chrome-0.1.6.zip'
DIG=str.maketrans('0123456789','०१२३४५६७८९')
exists=lambda p: os.path.exists(os.path.join(ROOT,p.lstrip('/')))
def size(p):
    b=os.path.getsize(os.path.join(ROOT,p.lstrip('/'))); return f'{b/1048576:.1f} MB'

PAGES=[('home',''),('projects','projects/'),('nepalos','nepalos/'),('slides','nepalos/slides/'),('lipi','lipi/'),
       ('contribute','contribute/'),('about','about/'),('brand','brand/')]
NAV=[('projects','projects/','Projects','परियोजना'),('nepalos','nepalos/','NepalOS','नेपालओएस'),('lipi','lipi/','Lipi','लिपि'),
     ('contribute','contribute/','Contribute','योगदान'),('about','about/','About','बारेमा'),('brand','brand/','Brand','ब्रान्ड')]
def href(lang,path): return ('/ne/' if lang=='ne' else '/')+path
EXT=' rel="noopener" target="_blank"'
RIDGE='<svg class="ridge" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 112 L180 96 L300 70 L360 84 L470 40 L560 74 L640 58 L760 18 L850 64 L930 50 L1040 80 L1130 60 L1250 88 L1360 78 L1440 92" fill="none" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></svg>'
MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'

def page(lang,key,path,title,desc,body,extra_js=''):
    T=lambda en,ne: ne if lang=='ne' else en
    other='en' if lang=='ne' else 'ne'
    cur=lambda k: k==key or (k=='nepalos' and key=='slides')
    nav=''.join(f'<li><a href="{href(lang,p)}"{" aria-current=\"page\"" if cur(k) else ""}>{T(en,ne)}</a></li>' for k,p,en,ne in NAV)
    brand=T('GovTech Nepal','गभटेक नेपाल')
    full=f'{title} · {brand}' if key!='home' else T('GovTech Nepal · Open-source technology for public service','गभटेक नेपाल · सार्वजनिक सेवाका लागि खुला स्रोत प्रविधि')
    u_en=SITE+'/'+(path or ''); u_ne=SITE+'/ne/'+(path or ''); u=u_ne if lang=='ne' else u_en
    lang_link='' if path is None else f'<a class="lang" href="{href(other,path)}" hreflang="{other}" lang="{other}">{"English" if lang=="ne" else "नेपाली"}</a>'
    alt='' if key=='404' else f'<link rel="canonical" href="{u}"><link rel="alternate" hreflang="en" href="{u_en}"><link rel="alternate" hreflang="ne" href="{u_ne}"><link rel="alternate" hreflang="x-default" href="{u_en}">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
{alt}
<meta property="og:site_name" content="GovTech Nepal"><meta property="og:title" content="{html.escape(full)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{u}"><meta property="og:image" content="{SITE}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0B1530" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<meta name="msapplication-TileColor" content="#003893"><meta name="msapplication-config" content="/browserconfig.xml">
<link rel="preload" href="/assets/fonts/Mukta-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Mukta-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<script>try{{var t=localStorage.getItem('gtn-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body class="p-{key}">
<a class="skip" href="#main">{T('Skip to content','मुख्य सामग्रीमा जानुहोस्')}</a>
<header class="site-header"><div class="wrap hdr">
  <a class="brand" href="{href(lang,'')}" aria-label="{T('GovTech Nepal, home','गभटेक नेपाल, गृहपृष्ठ')}">
    <img class="mark mark-light" src="/assets/brand/govtechnepal-mark.svg" alt="" width="44" height="44">
    <img class="mark mark-dark" src="/assets/brand/govtechnepal-mark-dark.svg" alt="" width="44" height="44">
    <span class="wm"><span class="wm-en" lang="en">GovTech <span>Nepal</span></span><span class="wm-ne" lang="ne">गभटेक नेपाल</span></span>
  </a>
  <nav class="nav" aria-label="{T('Main','मुख्य')}"><ul>{nav}</ul></nav>
  <div class="tools">{lang_link}
    <button class="theme-btn" type="button" aria-pressed="false" aria-label="{T('Dark mode','डार्क मोड')}" title="{T('Toggle dark mode','डार्क मोड खोल्नुहोस् वा बन्द गर्नुहोस्')}">{MOON}</button>
  </div>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="ftr">
    <p class="notice small"><strong>{T('Open source, community-led.','खुला स्रोत, समुदायद्वारा सञ्चालित।')}</strong> {T('GovTech Nepal is an independent community project. It is not an office of the Government of Nepal and does not speak for it.','गभटेक नेपाल एक स्वतन्त्र सामुदायिक परियोजना हो। यो नेपाल सरकारको कार्यालय होइन, र सरकारको तर्फबाट बोल्दैन।')}</p>
    <nav aria-label="{T('Footer','फुटर')}"><ul>{nav}<li><a href="{GITHUB}"{EXT}>GitHub</a></li></ul></nav>
  </div>
  <div class="fine"><span>© 2026 GovTech Nepal · govtechnepal.org</span><span>{T('Code: Apache-2.0 · Fonts: SIL OFL 1.1','कोड: Apache-2.0 · फन्ट: SIL OFL 1.1')}</span></div>
</div></footer>
<script src="/assets/js/site.js" defer></script>{extra_js}
</body>
</html>
'''

def head(lang,title,lead,crumbs=(),kicker=''):
    T=lambda en,ne: ne if lang=='ne' else en
    c=''.join(f' / <a href="{href(lang,p)}">{t}</a>' for t,p in crumbs)
    k=f'<p class="eyebrow">{kicker}</p>' if kicker else ''
    return f'<section class="page-head"><div class="wrap"><p class="crumb"><a href="{href(lang,"")}">{T("Home","गृहपृष्ठ")}</a>{c}</p>{k}<h1>{title}</h1><p class="lead">{lead}</p></div></section>'

def pic(src,alt,w=1280,h=800,cls='',lazy=True):
    base=src.rsplit('.',1)[0]
    return f'<picture><source srcset="{base}.webp" type="image/webp"><img class="{cls}" src="{base}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>'

# ---------- project data ----------
def projects(lang):
    T=lambda en,ne: ne if lang=='ne' else en
    return [
     dict(name=T('NepalOS','नेपालओएस'),badge=T('Prototype','प्रोटोटाइप'),live=True,url=href(lang,'nepalos/'),ext=False,
          tag=T('Powered by GovTechNepal','गभटेकनेपालद्वारा सञ्चालित'),
          text=T('A Nepali-first desktop on Debian 13 and KDE Plasma, with ONLYOFFICE, Kalimati and Nepali keyboards ready on day one.','डेबियन १३ र केडीई प्लाज्मामा आधारित नेपाली भाषामैत्री डेस्कटप: ओन्लीअफिस, कालिमाटी र नेपाली किबोर्ड पहिलो दिनदेखि नै तयार।'),
          img='/assets/img/nepalos/desktop-dark.jpg'),
     dict(name=T('Lipi','लिपि'),badge=T('Release 0.1.6','संस्करण ०.१.६'),live=True,url=href(lang,'lipi/'),ext=False,tag='Type Nepali',
          text=T('A free Nepali keyboard with Romanized and Traditional layouts, for Windows, macOS and Chrome.','रोमनाइज्ड र परम्परागत लेआउटसहितको निःशुल्क नेपाली किबोर्ड: विन्डोज, म्याकओएस र क्रोमका लागि।'),img=None),
     dict(name=T('Rasuwa Flood Bulletin','रसुवा बाढी बुलेटिन'),badge=T('Live','सञ्चालनमा'),live=True,url='https://nirajbhusal.github.io/rasuwa-flood-bulletin/index.html?lang=en',ext=True,
          tag=T('Public information during a disaster','विपद्का बेला सार्वजनिक सूचना'),
          text=T('A bilingual bulletin for the Rasuwa–Bhotekoshi flood: road status, alerts, relief and official notices in one place.','रसुवा–भोटेकोशी बाढीका लागि द्विभाषी बुलेटिन: सडकको अवस्था, सतर्कता, राहत र आधिकारिक सूचना एकै ठाउँमा।'),
          img='/assets/img/projects/rasuwa.jpg',repo='https://github.com/nirajbhusal/rasuwa-flood-bulletin'),
     dict(name=T('Mountain fonts','हिमाल फन्ट'),badge=T('In design','डिजाइन हुँदै'),live=False,url=None,ext=False,tag=T('Sagarmatha · Annapurna','सगरमाथा · अन्नपूर्ण'),
          text=T('Two open Devanagari and Latin typefaces, Sagarmatha and Annapurna, planned under the SIL Open Font License.','सगरमाथा र अन्नपूर्ण: SIL Open Font License अन्तर्गत ल्याउने योजना भएका दुई खुला देवनागरी र ल्याटिन टाइपफेस।'),img=None),
    ]

def card(p,lang,big=False):
    T=lambda en,ne: ne if lang=='ne' else en
    img=f'<div class="card-img">{pic(p["img"],"",1280,800)}</div>' if (big and p.get('img')) else ''
    ext=EXT if p['ext'] else ''
    title=f'<a class="stretch" href="{p["url"]}"{ext}>{p["name"]}{" <span class=\"sr\">"+T("(opens in a new tab)","(नयाँ ट्याबमा खुल्छ)")+"</span>" if p["ext"] else ""}</a>' if p['url'] else p['name']
    more=f'<span class="more" aria-hidden="true">{T("Visit site","साइट हेर्नुहोस्") if p["ext"] else T("Learn more","थप जान्नुहोस्")} {"↗" if p["ext"] else "→"}</span>' if p['url'] else ''
    repo=f'<a class="repo" href="{p["repo"]}"{EXT}>{T("Source on GitHub","GitHub मा स्रोत कोड")}</a>' if p.get('repo') and big else ''
    return f'<li class="card{" soon" if not p["live"] else ""}">{img}<div class="card-body"><span class="badge{" live" if p["live"] else ""}">{p["badge"]}</span><h3>{title}</h3><p class="tagline">{p["tag"]}</p><p>{p["text"]}</p>{more}{repo}</div></li>'

def grid(lang,big=False): return f'<ul class="grid{" big" if big else ""}" role="list">'+''.join(card(p,lang,big) for p in projects(lang))+'</ul>'

PRIN=[('Open by default','पूर्वनिर्धारित रूपमा खुला','Code, designs and decisions are public, so anyone can check, reuse and improve them.','कोड, डिजाइन र निर्णयहरू सार्वजनिक हुन्छन्, ताकि जोसुकैले जाँच्न, पुनः प्रयोग गर्न र सुधार्न सकियोस्।'),
      ('Nepali first','नेपाली पहिलो','Nepali language, Unicode text and Bikram Sambat dates work properly from day one.','नेपाली भाषा, युनिकोड र विक्रम संवत् मिति पहिलो दिनदेखि नै राम्ररी चल्छन्।'),
      ('Privacy and sovereignty','गोपनीयता र सार्वभौमिकता','No hidden tracking. Public data stays in Nepal, under Nepali control.','कुनै लुकेको ट्र्याकिङ छैन। सार्वजनिक डेटा नेपालमै, नेपालकै नियन्त्रणमा रहन्छ।'),
      ('Proven foundations','प्रमाणित आधार','We build on mature open-source projects such as Debian and KDE instead of reinventing them.','हामी डेबियन र केडीईजस्ता परिपक्व खुला स्रोत परियोजनामाथि निर्माण गर्छौं।'),
      ('Accessible to all','सबैका लागि पहुँचयोग्य','Usable by people of all abilities, in Nepali and English, on modest hardware.','सबै क्षमताका मानिसले, नेपाली र अङ्ग्रेजी दुवैमा, साधारण हार्डवेयरमा पनि प्रयोग गर्न सकिने।'),
      ('Community-led','समुदायको नेतृत्व','Anyone can contribute. Plans and discussions happen in the open.','जोसुकैले योगदान गर्न सक्नुहुन्छ। योजना र छलफल खुला रूपमा हुन्छन्।')]
def principles(lang,n=6):
    T=lambda en,ne: ne if lang=='ne' else en
    return '<ol class="principles">'+''.join(f'<li><h3>{T(a,b)}</h3><p>{T(c,d)}</p></li>' for a,b,c,d in PRIN[:n])+'</ol>'

# ---------- keyboards ----------
KB=json.load(open(os.path.join(ROOT,'demo/data/keyboards.json')))
ROWS=['`1234567890-=','qwertyuiop[]\\',"asdfghjkl;'",'zxcvbnm,./']
SHIFT=dict(zip('`1234567890-=[]\\;\',./','~!@#$%^&*()_+{}|:"<>?'))
def keyboard(layout,lang,label):
    m=KB[layout]['map']
    def out(c):
        o=m.get(c,'')
        return html.escape(o) if o.strip('\u200c\u200d') else ('ZWNJ' if o=='\u200c' else 'ZWJ' if o=='\u200d' else '')
    rows=[]
    for r in ROWS:
        keys=[]
        for c in r:
            s=SHIFT.get(c,c.upper())
            keys.append(f'<li><span class="k-lat">{html.escape(c.upper() if c.isalpha() else c)}</span><span class="k-sh" lang="ne">{out(s)}</span><span class="k-ne" lang="ne">{out(c)}</span></li>')
        rows.append(f'<ol class="kb-row">{"".join(keys)}</ol>')
    return f'<figure class="kb" aria-label="{html.escape(label)}"><div class="kb-scroll">{"".join(rows)}</div><figcaption>{label}</figcaption></figure>'

# ---------- slides ----------
SLIDES=[(1,'',''),(2,'',''),(3,'',''),(4,'',''),(6,'draft',''),(7,'',''),(8,'',''),(9,'draft',''),(10,'draft','')]
STITLE={1:('Title','शीर्षक'),2:('The problem today','आजको समस्या'),3:('The model: EU OS','नमुना: EU OS'),4:("What's inside",'यसमा के छ'),6:('Mass deployment','ठूलो स्तरमा जडान'),
        7:('Security and sovereignty','सुरक्षा र सार्वभौमिकता'),8:('Risks and responses','जोखिम र समाधान'),9:('Twelve months to version 1.0','संस्करण १.० सम्म बाह्र महिना'),10:('The ask','अनुरोध')}

def build(lang):
    T=lambda en,ne: ne if lang=='ne' else en
    d=lambda s: s.translate(DIG) if lang=='ne' else s
    out={}
    # HOME
    out['home']=(T('Home','गृहपृष्ठ'),T('GovTech Nepal: a community hub for open-source government technology for Nepal. NepalOS, Lipi and more.','गभटेक नेपाल: नेपालका लागि खुला स्रोत सरकारी प्रविधिको सामुदायिक केन्द्र। नेपालओएस, लिपि र थप।'),f'''
<section class="hero"><div class="wrap">
  <p class="eyebrow">{T("Open-source technology for Nepal's public sector","नेपालको सार्वजनिक क्षेत्रका लागि खुला स्रोत प्रविधि")}</p>
  <h1>{T("Open, Nepali-first technology for public service.","सार्वजनिक सेवाका लागि खुला र नेपाली भाषामैत्री प्रविधि।")}</h1>
  <p class="lead">{T("GovTech Nepal is a community hub for open-source projects that help public offices work better: in Nepali, on software everyone can inspect, improve and own.","गभटेक नेपाल सार्वजनिक कार्यालयहरूलाई अझ राम्रोसँग काम गर्न सघाउने खुला स्रोत परियोजनाहरूको सामुदायिक केन्द्र हो: नेपाली भाषामा, सबैले जाँच्न, सुधार्न र आफ्नो बनाउन सकिने सफ्टवेयरमा।")}</p>
  <div class="actions"><a class="btn btn-primary" href="{href(lang,"projects/")}">{T("Explore projects","परियोजनाहरू हेर्नुहोस्")}</a><a class="btn btn-ghost" href="{href(lang,"contribute/")}">{T("Contribute","योगदान गर्नुहोस्")}</a></div>
</div>{RIDGE}</section>
<section class="section alt" aria-labelledby="h-feat"><div class="wrap feature">
  <div class="feature-copy">
    <p class="eyebrow">{T("Flagship project","मुख्य परियोजना")}</p>
    <h2 id="h-feat">NepalOS</h2>
    <p class="tagline-lg">{T("Powered by GovTechNepal","गभटेकनेपालद्वारा सञ्चालित")}</p>
    <p>{T("A free, Nepali-first desktop built on Debian 13 and KDE Plasma. Kalimati 12 pt, Romanized and Traditional keyboards, the Bikram Sambat date and GIOMS are ready from the first login.","डेबियन १३ र केडीई प्लाज्मामा बनेको निःशुल्क, नेपाली भाषामैत्री डेस्कटप। कालिमाटी १२ पोइन्ट, रोमनाइज्ड र परम्परागत किबोर्ड, विक्रम संवत् मिति र जिआइओएमएस पहिलो लगइनदेखि नै तयार।")}</p>
    <div class="actions"><a class="btn btn-primary" href="/demo/">{T("Try the web demo","वेब डेमो चलाउनुहोस्")}</a><a class="btn btn-ghost" href="{href(lang,"nepalos/")}">{T("About NepalOS","नेपालओएसको बारेमा")}</a></div>
  </div>
  <div class="feature-shot">{pic("/assets/img/nepalos/desktop-dark.jpg",T("NepalOS desktop with an Everest wallpaper and the taskbar","सगरमाथाको वालपेपर र टास्कबारसहितको नेपालओएस डेस्कटप"),1280,800,"shot",False)}</div>
</div></section>
<section class="section" aria-labelledby="h-projects"><div class="wrap">
  <div class="sec-head"><div><h2 id="h-projects">{T("Projects","परियोजनाहरू")}</h2><p class="muted">{T("Every project is open source and built in the open.","हरेक परियोजना खुला स्रोत हो र खुला रूपमै बनाइन्छ।")}</p></div><a href="{href(lang,"projects/")}">{T("All projects","सबै परियोजना")} →</a></div>
  {grid(lang)}
</div></section>
<section class="section alt" aria-labelledby="h-prin"><div class="wrap">
  <div class="sec-head"><h2 id="h-prin">{T("How we work","हामी कसरी काम गर्छौं")}</h2><a href="{href(lang,"about/")}#principles">{T("All principles","सबै सिद्धान्त")} →</a></div>
  {principles(lang,3)}
</div></section>
<section class="section" aria-labelledby="h-join"><div class="wrap">
  <h2 id="h-join">{T("Build it with us","हामीसँगै निर्माण गर्नुहोस्")}</h2>
  <p class="lead">{T("Developers, translators, designers, testers and public servants are all welcome. You don’t need to write code to make a difference.","डेभलपर, अनुवादक, डिजाइनर, परीक्षक र सरकारी कर्मचारी सबैलाई स्वागत छ। फरक ल्याउन हजुरले कोड नै लेख्नुपर्छ भन्ने छैन।")}</p>
  <div class="actions"><a class="btn btn-primary" href="{href(lang,"contribute/")}">{T("Start contributing","योगदान सुरु गर्नुहोस्")}</a><a class="btn btn-ghost" href="{GITHUB}"{EXT}>GitHub ↗</a></div>
</div></section>''')
    # PROJECTS
    out['projects']=(T('Projects','परियोजनाहरू'),T('Open-source projects by the GovTech Nepal community: NepalOS, Lipi, Rasuwa Flood Bulletin and Mountain fonts.','गभटेक नेपाल समुदायका खुला स्रोत परियोजनाहरू: नेपालओएस, लिपि, रसुवा बाढी बुलेटिन र हिमाल फन्ट।'),
      head(lang,T('Projects','परियोजनाहरू'),T('Open tools for public service. Each one is open source, and each one needs collaborators.','सार्वजनिक सेवाका लागि खुला उपकरणहरू। हरेक खुला स्रोत हो, र हरेकलाई सहकर्मी चाहिन्छ।'))+
      f'<div class="wrap prose">{grid(lang,True)}<p class="small muted" style="margin-top:2rem">{T("Have an idea for a project? ","कुनै परियोजनाको विचार छ? ")}<a href="{href(lang,"contribute/")}#propose">{T("Propose it","प्रस्ताव गर्नुहोस्")}</a>.</p></div>')
    # NEPALOS
    shots=[('desktop-dark',T('Desktop with the Everest wallpaper','सगरमाथा वालपेपरसहितको डेस्कटप')),('about-window',T('About NepalOS: Debian 13, KDE Plasma, GIOMS and ONLYOFFICE','नेपालओएसबारे: डेबियन १३, केडीई प्लाज्मा, जिआइओएमएस र ओन्लीअफिस')),
           ('launcher',T('Application launcher','एप्लिकेसन लन्चर')),('chrome-gioms',T('Chrome opens GIOMS (gioms.gov.np) by default','क्रोममा जिआइओएमएस (gioms.gov.np) स्वतः खुल्छ')),
           ('chrome-bookmarks',T('Managed bookmarks for public services','सार्वजनिक सेवाका व्यवस्थित बुकमार्क')),('office-kalimati',T('Kalimati 12 pt as the default document font (screenshot from an earlier build with LibreOffice; ONLYOFFICE is now the default)','कालिमाटी १२ पोइन्ट पूर्वनिर्धारित कागजात फन्ट (लिब्रेअफिस भएको पुरानो बिल्डको स्क्रिनसट; अहिले ओन्लीअफिस पूर्वनिर्धारित छ)')),
           ('sddm-login',T('Login screen: NepalOS, Powered by GovTechNepal','लगइन स्क्रिन: नेपालओएस, गभटेकनेपालद्वारा सञ्चालित')),('ibus-switcher',T('Switching between Nepali keyboard layouts','नेपाली किबोर्ड लेआउटबीच फेरबदल'))]
    gal=''.join(f'<li><a href="/assets/img/nepalos/{f}.webp">{pic(f"/assets/img/nepalos/{f}.jpg",c)}</a><p>{c}</p></li>' for f,c in shots)
    out['nepalos']=(T('NepalOS','नेपालओएस'),T('NepalOS, Powered by GovTechNepal: a free, Nepali-first desktop on Debian 13 and KDE Plasma.','नेपालओएस, गभटेकनेपालद्वारा सञ्चालित: डेबियन १३ र केडीई प्लाज्मामा आधारित निःशुल्क, नेपाली भाषामैत्री डेस्कटप।'),
      head(lang,'NepalOS' if lang=='en' else 'नेपालओएस',T('A free, modern, Nepali-first desktop for public offices and everyone else. Built on Debian 13 and KDE Plasma.','सार्वजनिक कार्यालय र सबैका लागि निःशुल्क, आधुनिक र नेपाली भाषामैत्री डेस्कटप। डेबियन १३ र केडीई प्लाज्मामा निर्मित।'),
           [(T('Projects','परियोजना'),'projects/')],T('Powered by GovTechNepal','गभटेकनेपालद्वारा सञ्चालित'))+f'''
<div class="wrap prose"><div class="two"><div>
<div class="actions" style="margin-top:0"><a class="btn btn-primary" href="/demo/">{T("Try the web demo","वेब डेमो चलाउनुहोस्")}</a><a class="btn btn-ghost" href="{href(lang,"nepalos/slides/")}">{T("View the slides","स्लाइड हेर्नुहोस्")}</a></div>
<h2>{T("What NepalOS is","नेपालओएस के हो")}</h2>
<p>{T("NepalOS is a carefully configured Debian 13 (trixie) with the KDE Plasma desktop. It is not a new system written from scratch: it uses one of the most stable and widely trusted Linux distributions, with everything a Nepali office needs set up by default.","नेपालओएस केडीई प्लाज्मा डेस्कटपसहितको सावधानीपूर्वक मिलाइएको डेबियन १३ (ट्रिक्सी) हो। यो शून्यबाट लेखिएको नयाँ प्रणाली होइन: यसले विश्वका सबैभन्दा स्थिर र भरपर्दा लिनक्स वितरणमध्ये एक प्रयोग गर्छ, र नेपाली कार्यालयलाई चाहिने सबै कुरा पहिल्यै मिलाइएको हुन्छ।")}</p>
<h2>{T("What’s inside","यसमा के छ")}</h2>
<ul class="feature-list">
<li><b>{T("Modern KDE Plasma desktop","आधुनिक केडीई प्लाज्मा डेस्कटप")}</b><span>{T("Clean light and dark looks, Himalaya and heritage wallpapers.","सफा हल्का र गाढा रूप, हिमाल र सम्पदाका वालपेपर।")}</span></li>
<li><b>Google Chrome</b><span>{T("The default browser, with managed bookmarks for public services.","सार्वजनिक सेवाका व्यवस्थित बुकमार्कसहित पूर्वनिर्धारित ब्राउजर।")}</span></li>
<li><b>{T("ONLYOFFICE, Kalimati 12 pt","ओन्लीअफिस, कालिमाटी १२ पोइन्ट")}</b><span>{T("The default office suite; new documents start in Kalimati 12 pt.","पूर्वनिर्धारित अफिस सुइट; नयाँ कागजात कालिमाटी १२ पोइन्टमा सुरु हुन्छन्।")}</span></li>
<li><b>{T("Romanized and Traditional keyboards","रोमनाइज्ड र परम्परागत किबोर्ड")}</b><span>{T("Both Nepali layouts, with a one-click switch.","दुवै नेपाली लेआउट, एक क्लिकमा फेरबदल।")}</span></li>
<li><b>{T("GIOMS by default","जिआइओएमएस पूर्वनिर्धारित")}</b><span>{T("The browser opens gioms.gov.np, the government’s integrated office management system.","ब्राउजरमा सरकारको एकीकृत कार्यालय व्यवस्थापन प्रणाली gioms.gov.np खुल्छ।")}</span></li>
<li><b>{T("Bikram Sambat date","विक्रम संवत् मिति")}</b><span>{T("The clock shows the BS date in Nepali, alongside the AD date.","घडीमा नेपालीमा वि.सं. मिति, साथमा ई.सं. मिति।")}</span></li>
</ul>
<h2>{T("About Kalimati","कालिमाटीबारे")}</h2>
<p>{T("Kalimati is the font used for official Nepali documents, so NepalOS uses it as the default document font. Kalimati is not under an open licence. Its redistribution rights must be confirmed before a public release, and the open Noto Sans Devanagari is the fallback.","कालिमाटी आधिकारिक नेपाली कागजातमा प्रयोग हुने फन्ट हो, त्यसैले नेपालओएसले यसलाई पूर्वनिर्धारित कागजात फन्ट बनाएको छ। कालिमाटी खुला लाइसेन्समा छैन। सार्वजनिक संस्करणअघि यसको पुनर्वितरण अधिकार पक्का गर्नुपर्छ, र खुला नोटो सान्स देवनागरी विकल्पका रूपमा रहन्छ।")}</p>
<h2>{T("Download","डाउनलोड")}</h2>
<p><span class="badge">{T("Coming soon","छिट्टै आउँदैछ")}</span></p>
<p>{T("The installable ISO image is being tested and will be published here. Until then, the web demo shows the desktop in the browser.","इन्स्टल गर्न मिल्ने आइएसओ इमेज परीक्षण हुँदैछ र यहीँ प्रकाशित हुनेछ। त्यतिन्जेल वेब डेमोले ब्राउजरमै डेस्कटप देखाउँछ।")}</p>
</div>
<aside class="facts" aria-label="{T("Key facts","मुख्य तथ्य")}"><dl>
<dt>{T("Status","अवस्था")}</dt><dd>{T("Prototype","प्रोटोटाइप")} {d("0.2.0")}</dd>
<dt>{T("Base","आधार")}</dt><dd>Debian 13 (trixie)</dd>
<dt>{T("Desktop","डेस्कटप")}</dt><dd>KDE Plasma</dd>
<dt>{T("Office","अफिस")}</dt><dd>ONLYOFFICE · Kalimati {d("12")} pt</dd>
<dt>{T("Browser","ब्राउजर")}</dt><dd>Google Chrome · GIOMS</dd>
<dt>{T("ISO download","आइएसओ डाउनलोड")}</dt><dd>{T("Coming soon","छिट्टै आउँदैछ")}</dd>
<dt>{T("Source","स्रोत")}</dt><dd><a href="{GITHUB}"{EXT}>GitHub ↗</a></dd>
</dl></aside></div>
<h2 id="screenshots">{T("Screenshots","स्क्रिनसटहरू")}</h2>
<ul class="gallery" role="list">{gal}</ul>
<h2>{T("Slides","स्लाइड")}</h2>
<p>{T("The original NepalOS proposal deck, as a simple slide viewer.","नेपालओएसको मूल प्रस्ताव स्लाइड, सरल स्लाइड भ्युअरमा।")} <a href="{href(lang,"nepalos/slides/")}">{T("Open the slides","स्लाइड खोल्नुहोस्")} →</a></p>
</div>''')
    # SLIDES
    sl=''.join(f'<li class="slide" id="s{n}" data-n="{i+1}"><figure>{pic(f"/nepalos/slides/img/slide-{n:02d}.jpg",T("Slide","स्लाइड")+" "+d(str(n))+": "+T(*STITLE[n]),1600,901,"",i>1)}<figcaption><span>{d(str(i+1))} / {d(str(len(SLIDES)))} · {T(*STITLE[n])}</span>{"<span class=\"badge\">"+T("Early draft","प्रारम्भिक मस्यौदा")+"</span>" if f=="draft" else ""}</figcaption></figure></li>' for i,(n,f,_) in enumerate(SLIDES))
    dl=[('/downloads/nepalos/Nepal-OS-Proposal.pdf','PDF'),('/downloads/nepalos/Nepal-OS-Proposal.pptx','PowerPoint (.pptx)')]
    dls=' · '.join(f'<a href="{u}" download>{n}</a> <span class="muted">({size(u)})</span>' for u,n in dl if exists(u))
    out['slides']=(T('NepalOS slides','नेपालओएस स्लाइड'),T('The NepalOS proposal deck as a keyboard-navigable slide viewer.','किबोर्डबाट चलाउन मिल्ने स्लाइड भ्युअरमा नेपालओएस प्रस्ताव।'),
      head(lang,T('NepalOS slides','नेपालओएस स्लाइड'),T('The original proposal deck. Use the arrow keys or the buttons to move between slides.','मूल प्रस्ताव स्लाइड। स्लाइडबीच जान एरो किज वा बटन प्रयोग गर्नुहोस्।'),[('NepalOS' if lang=='en' else 'नेपालओएस','nepalos/')])+f'''
<div class="wrap prose">
<div class="viewer" id="viewer" aria-roledescription="{T("slide viewer","स्लाइड भ्युअर")}">
  <div class="viewer-bar" hidden><button type="button" class="btn btn-ghost" id="prev" aria-label="{T("Previous slide","अघिल्लो स्लाइड")}">← {T("Previous","अघिल्लो")}</button><span id="count" aria-live="polite"></span><button type="button" class="btn btn-ghost" id="next" aria-label="{T("Next slide","अर्को स्लाइड")}">{T("Next","अर्को")} →</button></div>
  <ol class="slides" role="list" tabindex="0" aria-label="{T("Slides","स्लाइडहरू")}">{sl}</ol>
</div>
<p class="notice small">{T("This deck is an early draft. Slides marked “Early draft” describe ideas, such as per-ministry editions, that are no longer planned: NepalOS ships as one edition, Powered by GovTechNepal. One slide on per-ministry branding is left out.","यो स्लाइड प्रारम्भिक मस्यौदा हो। “प्रारम्भिक मस्यौदा” चिह्न भएका स्लाइडमा मन्त्रालयअनुसारका संस्करणजस्ता अब योजनामा नरहेका विचार छन्: नेपालओएस एउटै संस्करणमा आउँछ, गभटेकनेपालद्वारा सञ्चालित। मन्त्रालयअनुसार ब्रान्डिङबारेको एउटा स्लाइड हटाइएको छ।")}</p>
<p>{T("Download the full deck","पूरा स्लाइड डाउनलोड गर्नुहोस्")}: {dls}</p>
</div>''','<script src="/assets/js/slides.js" defer></script>')
    # LIPI
    def dlrow(url,label,note,ext=False):
        if ext: return f'<li><a class="btn btn-primary" href="{url}"{EXT}>{label} ↗</a><span class="muted small">{note}</span></li>'
        if exists(url): return f'<li><a class="btn btn-primary" href="{url}" download>{label}</a><span class="muted small">{note} · {size(url)}</span></li>'
        return f'<li><span class="btn btn-disabled" aria-disabled="true">{label}</span><span class="muted small">{T("Coming soon","छिट्टै आउँदैछ")}</span></li>'
    out['lipi']=(T('Lipi','लिपि'),T('Lipi: Type Nepali. A free Nepali keyboard with Romanized and Traditional layouts for Windows, macOS and Chrome.','लिपि: नेपाली टाइप गर्नुहोस्। विन्डोज, म्याकओएस र क्रोमका लागि रोमनाइज्ड र परम्परागत लेआउटसहितको निःशुल्क नेपाली किबोर्ड।'),
      head(lang,T('Lipi','लिपि'),T('A free keyboard for writing correct Unicode Nepali in any app, in the layout you already know.','हजुरलाई पहिल्यै परिचित लेआउटमा, जुनसुकै एपमा शुद्ध युनिकोड नेपाली लेख्ने निःशुल्क किबोर्ड।'),[(T('Projects','परियोजना'),'projects/')],'Type Nepali')+f'''
<div class="wrap prose"><div class="two"><div>
<h2 id="download">{T("Download Lipi 0.1.6","लिपि ०.१.६ डाउनलोड")}</h2>
<ul class="downloads" role="list">
{dlrow(LIPI_WIN,T("Windows installer","विन्डोज इन्स्टलर"),T("84 MB, hosted on Google Drive","८४ MB, गुगल ड्राइभमा"),True)}
{dlrow(LIPI_MAC,T("macOS (.dmg)","म्याकओएस (.dmg)"),T("macOS disk image","म्याकओएस डिस्क इमेज"))}
{dlrow(LIPI_CHROME,T("Chrome extension (.zip)","क्रोम एक्सटेन्सन (.zip)"),T("Load unpacked in Chrome","क्रोममा Load unpacked गर्नुहोस्"))}
</ul>
<h2>{T("Two layouts","दुई लेआउट")}</h2>
<p>{T("Romanized: type Nepali the way it sounds on an English keyboard (k → क, a → ा). Traditional: the classic Nepali typewriter layout used in offices. Switch at any time.","रोमनाइज्ड: अङ्ग्रेजी किबोर्डमा उच्चारणअनुसार नेपाली टाइप गर्नुहोस् (k → क, a → ा)। परम्परागत: कार्यालयमा प्रयोग हुने पुरानो नेपाली टाइपराइटर लेआउट। जुनसुकै बेला फेर्न सकिन्छ।")}</p>
{keyboard("romanized",lang,T("Romanized layout. Large: key without Shift. Small: with Shift.","रोमनाइज्ड लेआउट। ठूलो: सिफ्टबिना। सानो: सिफ्टसहित।"))}
{keyboard("traditional",lang,T("Traditional layout. Large: key without Shift. Small: with Shift.","परम्परागत लेआउट। ठूलो: सिफ्टबिना। सानो: सिफ्टसहित।"))}
<h2>{T("Install","इन्स्टल गर्ने तरिका")}</h2>
<h3>Windows</h3>
<ol><li>{T("Download the installer and run it.","इन्स्टलर डाउनलोड गरेर चलाउनुहोस्।")}</li><li>{T("If Windows SmartScreen appears, choose More info, then Run anyway.","विन्डोज स्मार्टस्क्रिन देखियो भने More info, अनि Run anyway छान्नुहोस्।")}</li><li>{T("Switch to Lipi with Windows + Space, then pick Romanized or Traditional.","Windows + Space थिचेर लिपिमा जानुहोस्, अनि रोमनाइज्ड वा परम्परागत छान्नुहोस्।")}</li></ol>
<h3>macOS</h3>
<ol><li>{T("Open the .dmg and double-click Install Lipi. It installs the keyboard and turns it on.",".dmg खोलेर Install Lipi मा डबल-क्लिक गर्नुहोस्। यसले किबोर्ड इन्स्टल गरेर सक्रिय गर्छ।")}</li><li>{T("If macOS says the app is from an unidentified developer, right-click it and choose Open.","एप अज्ञात डेभलपरको हो भनेर म्याकओएसले देखायो भने राइट-क्लिक गरेर Open छान्नुहोस्।")}</li><li>{T("Choose Lipi from the input menu in the menu bar.","मेनु बारको इनपुट मेनुबाट लिपि छान्नुहोस्।")}</li></ol>
<h3>Chrome</h3>
<ol><li>{T("Unzip the file.","फाइल अनजिप गर्नुहोस्।")}</li><li>{T("Open chrome://extensions and turn on Developer mode.","chrome://extensions खोलेर Developer mode सक्रिय गर्नुहोस्।")}</li><li>{T("Click Load unpacked and choose the folder that contains manifest.json.","Load unpacked थिचेर manifest.json भएको फोल्डर छान्नुहोस्।")}</li><li>{T("Pin Lipi. Use the popup or side panel to switch layouts.","लिपिलाई पिन गर्नुहोस्। लेआउट फेर्न पपअप वा साइड प्यानल प्रयोग गर्नुहोस्।")}</li></ol>
</div>
<aside class="facts" aria-label="{T("Quality","गुणस्तर")}"><dl>
<dt>{T("Version","संस्करण")}</dt><dd>{d("0.1.6")}</dd>
<dt>{T("Automated tests","स्वचालित परीक्षण")}</dt><dd>{T("About 16,000 · 0 failures","करिब १६,००० · ० असफल")}</dd>
<dt>{T("Windows tests","विन्डोज परीक्षण")}</dt><dd>{T("1,543 · 0 failures","१,५४३ · ० असफल")}</dd>
<dt>{T("Layouts","लेआउट")}</dt><dd>{T("Romanized · Traditional","रोमनाइज्ड · परम्परागत")}</dd>
<dt>{T("Platforms","प्लेटफर्म")}</dt><dd>Windows · macOS · Chrome</dd>
<dt>{T("Also in","यसमा पनि")}</dt><dd><a href="{href(lang,"nepalos/")}">{T("NepalOS","नेपालओएस")}</a></dd>
</dl></aside></div></div>''')
    # CONTRIBUTE
    WAYS=[('Write code','कोड लेख्नुहोस्','Fix bugs, package software for Debian, improve the keyboards.','बग सच्याउनुहोस्, डेबियनका लागि सफ्टवेयर प्याकेज गर्नुहोस्, किबोर्ड सुधार्नुहोस्।'),
          ('Translate and review','अनुवाद र समीक्षा','Make interfaces and guides read naturally in Nepali.','इन्टरफेस र गाइडलाई नेपालीमा स्वाभाविक बनाउनुहोस्।'),
          ('Test','परीक्षण','Try NepalOS and Lipi on the hardware and apps offices actually use, and report what breaks.','कार्यालयले प्रयोग गर्ने हार्डवेयर र एपमा नेपालओएस र लिपि चलाएर के बिग्रियो, जानकारी दिनुहोस्।'),
          ('Design and accessibility','डिजाइन र पहुँचयोग्यता','Help make every screen clear and usable for all, including the Mountain fonts.','हिमाल फन्टसहित हरेक स्क्रिन सबैका लागि स्पष्ट र प्रयोगयोग्य बनाउन सघाउनुहोस्।'),
          ('Write documentation','डकुमेन्टेसन लेख्नुहोस्','Guides for installers, IT staff and everyday users.','इन्स्टल गर्ने, आईटी कर्मचारी र सामान्य प्रयोगकर्ताका लागि गाइड।'),
          ('Share what offices need','कार्यालयको आवश्यकता बताउनुहोस्','Public servants: tell us where software gets in the way.','सरकारी कर्मचारीहरू: सफ्टवेयरले कहाँ अप्ठ्यारो पार्छ, हामीलाई बताउनुहोस्।')]
    out['contribute']=(T('Contribute','योगदान'),T('Contribute to GovTech Nepal: code, translation, testing, design and documentation. Apache-2.0 code, OFL fonts.','गभटेक नेपालमा योगदान: कोड, अनुवाद, परीक्षण, डिजाइन र डकुमेन्टेसन।'),
      head(lang,T('Contribute','योगदान गर्नुहोस्'),T('Everything here is open source, and there is a place for you whether you write code or not.','यहाँ सबै खुला स्रोत हो। हजुर कोड लेख्नुहुन्छ वा लेख्नुहुन्न, हजुरका लागि ठाउँ छ।'))+f'''
<div class="wrap prose">
<div class="callout"><div><h2 style="margin:0 0 .4rem">GitHub</h2><p class="muted" style="margin:0">{T("Issues, plans and code live on GitHub. Start by reading open issues or opening a new one.","इस्यु, योजना र कोड GitHub मा छन्। खुला इस्यु पढेर वा नयाँ इस्यु खोलेर सुरु गर्नुहोस्।")}</p></div><a class="btn btn-primary" href="{GITHUB}"{EXT}>{T("Open on GitHub","GitHub मा खोल्नुहोस्")} ↗</a></div>
<h2>{T("How to help","कसरी सघाउने")}</h2>
<ul class="feature-list">{''.join(f'<li><b>{T(a,b)}</b><span>{T(c,e)}</span></li>' for a,b,c,e in WAYS)}</ul>
<h2>{T("Getting started","सुरु गर्ने तरिका")}</h2>
<ol><li>{T("Pick a project: NepalOS, Lipi, the Rasuwa Flood Bulletin or the Mountain fonts.","एउटा परियोजना छान्नुहोस्: नेपालओएस, लिपि, रसुवा बाढी बुलेटिन वा हिमाल फन्ट।")}</li><li>{T("Open an issue describing what you want to do, or comment on an existing one.","हजुर के गर्न चाहनुहुन्छ भनेर इस्यु खोल्नुहोस्, वा भइरहेको इस्युमा प्रतिक्रिया दिनुहोस्।")}</li><li>{T("Send a pull request. Small, focused changes are easiest to review.","पुल रिक्वेस्ट पठाउनुहोस्। साना र केन्द्रित परिवर्तन समीक्षा गर्न सजिलो हुन्छ।")}</li></ol>
<h2 id="licences">{T("Licences","लाइसेन्स")}</h2>
<ul>
<li>{T("Code: Apache License 2.0, unless a file says otherwise.","कोड: Apache License 2.0, फाइलमा अर्को उल्लेख नभएसम्म।")}</li>
<li>{T("Fonts: SIL Open Font License 1.1 (OFL). This site uses Mukta (OFL); the Mountain fonts will be released under the OFL.","फन्ट: SIL Open Font License 1.1 (OFL)। यो साइटले मुक्ता (OFL) प्रयोग गर्छ; हिमाल फन्ट पनि OFL मै आउनेछन्।")}</li>
<li>{T("Keyboard layouts in Lipi build on MIT-licensed Keyman layouts.","लिपिका किबोर्ड लेआउट MIT लाइसेन्सका किम्यान लेआउटमा आधारित छन्।")}</li>
<li>{T("Kalimati, the font for official documents, is not openly licensed and is not covered by these licences.","आधिकारिक कागजातको फन्ट कालिमाटी खुला लाइसेन्समा छैन, र यी लाइसेन्सभित्र पर्दैन।")}</li>
</ul>
<h2 id="propose">{T("Propose a project","परियोजना प्रस्ताव गर्नुहोस्")}</h2>
<p>{T("Good proposals solve a real problem for a public office, can be open source, and build on existing tools where possible. Open a GitHub issue that describes the problem first, then the idea.","राम्रो प्रस्तावले सार्वजनिक कार्यालयको वास्तविक समस्या समाधान गर्छ, खुला स्रोत हुन सक्छ, र सम्भव भएसम्म भइरहेका उपकरणमाथि निर्माण गर्छ। पहिले समस्या, त्यसपछि विचार लेखेर GitHub इस्यु खोल्नुहोस्।")}</p>
<p class="notice">{T("Please don’t share personal or confidential government data in any public issue or discussion.","कृपया कुनै पनि सार्वजनिक इस्यु वा छलफलमा व्यक्तिगत वा गोप्य सरकारी डेटा नबाँड्नुहोस्।")}</p>
</div>''')
    # ABOUT
    out['about']=(T('About','बारेमा'),T('About GovTech Nepal, an independent open-source community for public-sector technology in Nepal.','नेपालको सार्वजनिक क्षेत्रका लागि खुला स्रोत प्रविधिमा काम गर्ने स्वतन्त्र समुदाय, गभटेक नेपालबारे।'),
      head(lang,T('About GovTech Nepal','गभटेक नेपालको बारेमा'),T('An independent, open-source community building technology for Nepal’s public sector.','नेपालको सार्वजनिक क्षेत्रका लागि प्रविधि बनाउने स्वतन्त्र, खुला स्रोत समुदाय।'))+f'''
<div class="wrap prose">
<h2>{T("What we do","हामी के गर्छौं")}</h2>
<p>{T("GovTech Nepal is the umbrella for open-source projects that make everyday public work simpler, more affordable and more Nepali: NepalOS, the Lipi keyboard, the Rasuwa Flood Bulletin and the Mountain fonts.","गभटेक नेपाल दैनिक सार्वजनिक कामलाई सरल, सस्तो र नेपाली भाषामैत्री बनाउने खुला स्रोत परियोजनाहरूको छाता हो: नेपालओएस, लिपि किबोर्ड, रसुवा बाढी बुलेटिन र हिमाल फन्ट।")}</p>
<h2>{T("Independent","स्वतन्त्र")}</h2>
<p class="notice"><strong>{T("We are not a Government of Nepal office.","हामी नेपाल सरकारको कार्यालय होइनौँ।")}</strong> {T("We do not speak for any ministry and do not use the national emblem. Whether government adopts any of this work is government’s decision.","हामी कुनै मन्त्रालयको तर्फबाट बोल्दैनौँ, र राष्ट्रिय निशान प्रयोग गर्दैनौँ। यो काम सरकारले अपनाउने वा नअपनाउने निर्णय सरकारकै हो।")}</p>
<h2>{T("Who is behind it","यसका पछाडि को छन्")}</h2>
<p>{T("GovTech Nepal was started by Niraj Bhusal and is open to everyone who wants to help.","गभटेक नेपाल निरज भुसालले सुरु गरेका हुन्, र सघाउन चाहने सबैका लागि खुला छ।")}</p>
<h2 id="principles">{T("Principles","सिद्धान्तहरू")}</h2>
{principles(lang)}
<h2>{T("The name","नाम")}</h2>
<p>{T("“GovTech” is short for government technology. In Nepali we write it गभटेक नेपाल.","“GovTech” गभर्नमेन्ट टेक्नोलोजी (सरकारी प्रविधि) को छोटो रूप हो। नेपालीमा हामी यसलाई गभटेक नेपाल लेख्छौँ।")}</p>
</div>''')
    # BRAND
    files=[('govtechnepal-logo-light',T('Horizontal logo, light','तेर्सो लोगो, हल्का'),False),('govtechnepal-logo-dark',T('Horizontal logo, dark','तेर्सो लोगो, गाढा'),True)]
    tiles=''.join(f'<figure class="tile{" dark" if dk else ""}"><img src="/assets/brand/{f}.svg" alt="{c}" width="620" height="200" loading="lazy"><figcaption class="tile-cap"><span>{c}</span><span><a href="/assets/brand/{f}.svg" download>SVG</a> · <a href="/assets/brand/{f}.png" download>PNG</a></span></figcaption></figure>' for f,c,dk in files)
    marks=[('govtechnepal-mark',T('Mark','चिह्न'),'govtechnepal-mark-512.png'),('govtechnepal-mark-dark',T('Mark, dark backgrounds','चिह्न, गाढा पृष्ठभूमि'),'govtechnepal-mark-dark-512.png')]
    mk=''.join(f'<figure><img src="/assets/brand/{f}.svg" alt="" width="72" height="72" loading="lazy"><figcaption>{c}<br><a href="/assets/brand/{f}.svg" download>SVG</a> · <a href="/assets/brand/{p}" download>PNG 512</a></figcaption></figure>' for f,c,p in marks)
    mk+=f'<figure><img src="/favicon.svg" alt="" width="72" height="72" loading="lazy"><figcaption>{T("Favicon","फेभिकन")}<br><a href="/favicon.svg" download>SVG</a> · <a href="/favicon.ico" download>ICO</a></figcaption></figure>'
    mk+=f'<figure><img src="/android-chrome-192x192.png" alt="" width="72" height="72" loading="lazy"><figcaption>{T("App icons","एप आइकन")}<br><a href="/apple-touch-icon.png" download>180</a> · <a href="/android-chrome-192x192.png" download>192</a> · <a href="/android-chrome-512x512.png" download>512</a></figcaption></figure>'
    sw=[('Deep blue','गाढा नीलो','#003893',T('Primary','मुख्य')),('Crimson','सिम्रिक','#DC143C',T('Accent, use sparingly','सहायक, थोरै मात्र')),('Navy','नेभी','#0B1530',T('Text and dark backgrounds','पाठ र गाढा पृष्ठभूमि')),('Off-white','हल्का सेतो','#F7F5F0',T('Light backgrounds','हल्का पृष्ठभूमि'))]
    out['brand']=(T('Brand','ब्रान्ड'),T('GovTech Nepal logo files, colours and typography.','गभटेक नेपालका लोगो फाइल, रङ र टाइपोग्राफी।'),
      head(lang,T('Brand','ब्रान्ड'),T('Logo files, colours and type for GovTech Nepal. Free to use when referring to the project.','गभटेक नेपालका लोगो फाइल, रङ र अक्षर। परियोजनाको सन्दर्भमा प्रयोग गर्न निःशुल्क।'))+f'''
<div class="wrap prose">
<h2>{T("Logo","लोगो")}</h2>
<p>{T("The logo is the ग tile with the Mukta wordmark. Use the dark version on dark backgrounds.","लोगो मुक्ता वर्डमार्कसहितको ग टाइल हो। गाढा पृष्ठभूमिमा गाढा संस्करण प्रयोग गर्नुहोस्।")}</p>
<div class="logo-tiles">{tiles}</div>
<h2>{T("Mark and icons","चिह्न र आइकन")}</h2>
<div class="marks">{mk}</div>
<p class="small muted" style="margin-top:1rem">{T("Social share card:","सामाजिक सञ्जाल कार्ड:")} <a href="/og-image.png" download>og-image.png (1200×630)</a></p>
<h2>{T("Colour","रङ")}</h2>
<div class="swatches">{''.join(f'<div class="sw"><i style="background:{h}{";box-shadow:inset 0 -1px 0 #E2E0DA" if h=="#F7F5F0" else ""}"></i><div><b>{T(a,b)}</b><code>{h}</code><br><span class="muted">{u}</span></div></div>' for a,b,h,u in sw)}</div>
<h2>{T("Typography","टाइपोग्राफी")}</h2>
<p>{T("Mukta is used for everything: headings, body text and the wordmark. It covers Devanagari and Latin and is open source (SIL OFL). Kalimati is the font for official Nepali documents, used inside NepalOS, not on this site.","शीर्षक, मुख्य पाठ र वर्डमार्क सबैमा मुक्ता प्रयोग हुन्छ। यसले देवनागरी र ल्याटिन दुवै समेट्छ र खुला स्रोत (SIL OFL) हो। कालिमाटी आधिकारिक नेपाली कागजातको फन्ट हो, जुन नेपालओएसभित्र प्रयोग हुन्छ, यो साइटमा होइन।")}</p>
<div class="logo-tiles">
<div class="type-sample"><span class="muted small">Mukta · {T("primary","मुख्य")}</span><p class="big">GovTech Nepal</p><p class="big" lang="ne">गभटेक नेपाल</p></div>
<div class="type-sample"><span class="muted small">Khand · {T("alternative, not used on the site","विकल्प, साइटमा प्रयोग हुँदैन")}</span><p class="big khand">GovTech Nepal</p><p class="big khand" lang="ne">गभटेक नेपाल</p></div>
</div>
<p class="small muted" style="margin-top:1rem">{T("Alternative lockup with the Khand wordmark:","खण्ड वर्डमार्कसहितको वैकल्पिक लकअप:")} <a href="/assets/brand/govtechnepal-logo-khand-light.svg" download>{T("light","हल्का")}</a> · <a href="/assets/brand/govtechnepal-logo-khand-dark.svg" download>{T("dark","गाढा")}</a></p>
<h2>{T("Usage","प्रयोग")}</h2>
<ul class="rules">
<li>{T("Keep clear space around the logo equal to half the height of the mark.","लोगोवरिपरि चिह्नको आधा उचाइ बराबर खाली ठाउँ राख्नुहोस्।")}</li>
<li>{T("Don’t recolour, stretch, rotate or add effects.","रङ नफेर्नुहोस्, नतन्काउनुहोस्, नघुमाउनुहोस्, प्रभाव नथप्नुहोस्।")}</li>
<li>{T("Never combine the logo with the national emblem or flag.","लोगोलाई राष्ट्रिय निशान वा झण्डासँग कहिल्यै नमिसाउनुहोस्।")}</li>
<li>{T("Don’t use it in a way that suggests official government endorsement.","सरकारी आधिकारिक समर्थन जनाउने गरी प्रयोग नगर्नुहोस्।")}</li>
<li>{T("Minimum size: 16 px for the mark alone, 120 px wide for the full logo.","न्यूनतम आकार: चिह्न मात्र १६ पिक्सेल, पूरा लोगो १२० पिक्सेल चौडा।")}</li>
<li>{T("Crimson is an accent: keep it small.","सिम्रिक सहायक रङ हो: थोरै मात्र प्रयोग गर्नुहोस्।")}</li>
</ul>
</div>''')
    return out

urls=[]
for lang in ('en','ne'):
    content=build(lang)
    for key,path in PAGES:
        v=content[key]; title,desc,body=v[:3]; js=v[3] if len(v)>3 else ''
        dd=os.path.join(ROOT,'ne' if lang=='ne' else '',path); os.makedirs(dd,exist_ok=True)
        open(os.path.join(dd,'index.html'),'w').write(page(lang,key,path,title,desc,body,js))
        urls.append(SITE+('/ne/' if lang=='ne' else '/')+path)
b='<section class="page-head"><div class="wrap"><h1>Page not found · पृष्ठ भेटिएन</h1><p class="lead">The page you were looking for doesn’t exist. <a href="/">Go to the home page</a>.</p><p class="lead" lang="ne">हजुरले खोज्नुभएको पृष्ठ भेटिएन। <a href="/ne/">गृहपृष्ठमा जानुहोस्</a>।</p></div></section>'
open(os.path.join(ROOT,'404.html'),'w').write(page('en','404',None,'Page not found','Page not found',b))
urls.append(SITE+'/demo/')
open(os.path.join(ROOT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n')
open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('built',len(urls),'urls')
