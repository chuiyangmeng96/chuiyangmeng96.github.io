#!/usr/bin/env python3
"""Build the static website using only the Python standard library."""

import hashlib
import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://chuiyangmeng96.github.io"
PAPERS = json.loads((ROOT / "data/publications.json").read_text())
NEWS = sorted(json.loads((ROOT / "data/news.json").read_text()), key=lambda item: item["date"], reverse=True)
TALKS = sorted(json.loads((ROOT / "data/talks.json").read_text()), key=lambda item: item["date"], reverse=True)
ASSET_VERSIONS = {
    name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:10]
    for name in ("styles.css", "script.js")
}


def e(value):
    return escape(str(value), quote=True)


def citation(p):
    fields = {
        "title": "{" + p["title"] + "}",
        "author": " and ".join(p["authors"]),
        "year": p["year"],
    }
    if p["type"] == "preprint":
        fields["note"] = p["status"]
    else:
        fields["journal" if p["type"] == "journal" else "booktitle"] = p["venue"]
    for field in ("volume", "number"):
        if p.get(field):
            fields[field] = p[field]
    if p.get("doi"):
        fields["doi"] = p["doi"]
    if p.get("arxiv"):
        fields["url"] = p["arxiv"]
    if p.get("arxivId"):
        fields["eprint"] = p["arxivId"]
        fields["archivePrefix"] = "arXiv"
    kind = {"journal": "article", "conference": "inproceedings", "preprint": "unpublished"}[p["type"]]
    if p["type"] == "preprint" and p.get("arxivId"):
        kind = "misc"
    key = f"{p['authors'][0].split()[-1].lower()}{p['year']}{p['id'].replace('-', '')}"
    return f"@{kind}{{{key},\n" + ",\n".join(
        f"  {key} = {{{value}}}" for key, value in fields.items()
    ) + "\n}"


def resource(label, href):
    return f'<a class="paper-link" href="{e(href)}" target="_blank" rel="noopener">{label} <span aria-hidden="true">↗</span></a>'


def paper(p):
    authors = ", ".join(
        f"<strong>{e(author)}</strong>" if author == "Chuiyang Meng" else e(author)
        for author in p["authors"]
    )
    links = []
    if p.get("pdf"):
        links.append(resource("PDF", p["pdf"]))
    if p.get("arxiv"):
        links.append(resource("arXiv", p["arxiv"]))
    if p.get("doi"):
        links.append(resource("Publisher", "https://doi.org/" + p["doi"]))
    links.append(f'''<details class="citation"><summary>BibTeX</summary>
      <div class="citation-content"><pre>{e(citation(p))}</pre><button class="copy-citation" type="button" hidden>Copy citation</button></div></details>''')
    figure = ""
    if p.get("figure"):
        figure = f'''<div class="paper-figure">
          <a class="figure-trigger" href="{e(p['figure'])}" data-preview="{e(p['id'])}" aria-label="Enlarge figure: {e(p['title'])}">
            <img src="{e(p['thumbnail'])}" alt="{e(p['figureCaption'])}" width="680" height="440" loading="lazy">
            <span class="figure-hint"><span aria-hidden="true">⊕</span> View figure</span>
          </a>
          <template id="preview-{e(p['id'])}">
            <img class="preview-image" src="{e(p['figure'])}" alt="{e(p['figureCaption'])}">
            <div class="preview-copy"><p class="eyebrow">{e(p['figureCaption'])}</p>
              <h2 id="preview-title">{e(p['title'])}</h2><p>{e(p['explanation'])}</p>
              <a class="text-link" href="{e(p['pdf'])}" target="_blank" rel="noopener">Read the paper (PDF) ↗</a>
              <a class="text-link" href="{e(p['figure'])}" target="_blank" rel="noopener">Full-size figure ↗</a>
            </div>
          </template>
        </div>'''
    venue = (
        f'<span class="venue-name" title="{e(p["venue"])}" '
        f'aria-label="{e(p["venue"])}, {p["year"]}">'
        f'{e(p.get("venueShort", p["venue"]))} · {p["year"]}</span>'
    )
    if p.get("volume"):
        details = f'Vol. {p["volume"]}'
        if p.get("number"):
            details += f', no. {p["number"]}'
        venue += f' <span class="venue-details">{e(details)}</span>'
    if p.get("status"):
        venue += f' <span class="paper-status">{e(p["status"])}</span>'
    if p.get("acceptanceRate") is not None:
        venue += f' <span class="acceptance-rate">Acceptance rate: {e(p["acceptanceRate"])}%</span>'
    return f'''<article class="paper{'' if figure else ' paper-text-only'}" id="{e(p['id'])}" data-selected="{str(p['selected']).lower()}" data-topic="{e(p['topic'])}">
      <div class="paper-content"><h3>{e(p['title'])}</h3><p class="paper-authors">{authors}</p>
        <p class="paper-venue">{venue}</p>
        <p class="paper-summary">{e(p['summary'])}</p><div class="paper-links">{''.join(links)}</div>
      </div>{figure}</article>'''


def canonical_url(filename):
    # The legacy skills page repeats the skills section on the background page.
    if filename == "skills.html":
        filename = "experience.html"
    return SITE_URL + ("/" if filename == "index.html" else "/" + filename)


def profile_schema(description):
    profile = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "@id": SITE_URL + "/#profile",
        "url": SITE_URL + "/",
        "name": "Chuiyang Meng",
        "description": description,
        "mainEntity": {
            "@type": "Person",
            "@id": SITE_URL + "/#person",
            "name": "Chuiyang Meng",
            "url": SITE_URL + "/",
            "image": SITE_URL + "/life-photo-1.jpg",
            "jobTitle": "Postdoctoral Research Fellow",
            "worksFor": {"@type": "Organization", "name": "Simon Fraser University"},
            "email": "mailto:chuiyang_meng@sfu.ca",
            "knowsAbout": [
                "Foundation models", "Mechanistic interpretability", "Multi-agent systems",
                "Distributed and edge learning", "Communications and networks",
            ],
            "sameAs": [
                "https://orcid.org/0009-0000-9381-4916",
                "https://scholar.google.com/citations?user=MLB0NZsAAAAJ",
                "https://www.linkedin.com/in/chuiyang-meng-b54a48185",
                "https://github.com/chuiyangmeng96",
            ],
        },
    }
    # Keep JSON valid while preventing an embedded HTML closing tag.
    payload = json.dumps(profile, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'


def page(title, active, description, content, filename):
    canonical = canonical_url(filename)
    is_home = filename == "index.html"
    page_title = "Chuiyang Meng | Researcher at Simon Fraser University" if is_home else f"{title} | Chuiyang Meng"
    structured_data = profile_schema(description) if is_home else ""
    search_verification = '<meta name="google-site-verification" content="m0zgf31Iz2LRbnQKTFkeggcKBdc-xlt-MZMDY2JR3xY">' if is_home else ""
    nav = []
    for key, name, href in [
        ("about", "About", "./"),
        ("publications", "Publications", "publications.html"),
        ("background", "Background", "experience.html"),
        ("teaching", "Teaching & service", "teaching.html"),
    ]:
        current = ' aria-current="page"' if active == key else ""
        nav.append(f'<a href="{href}"{current}>{e(name)}</a>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(page_title)}</title><meta name="description" content="{e(description)}">
<meta name="author" content="Chuiyang Meng"><link rel="canonical" href="{e(canonical)}">
{search_verification}
<meta name="theme-color" content="#ffffff"><meta property="og:title" content="{e(page_title)}">
<meta property="og:description" content="{e(description)}"><meta property="og:type" content="{'profile' if is_home else 'website'}">
<meta property="og:url" content="{e(canonical)}"><meta property="og:site_name" content="Chuiyang Meng">
<meta property="og:image" content="{SITE_URL}/life-photo-1.jpg"><meta property="og:image:alt" content="Chuiyang Meng">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(page_title)}">
<meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{SITE_URL}/life-photo-1.jpg"><meta name="twitter:image:alt" content="Chuiyang Meng">
{structured_data}
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css?v={ASSET_VERSIONS['styles.css']}"><script src="script.js?v={ASSET_VERSIONS['script.js']}" defer></script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header container"><a class="site-name" href="./">Chuiyang Meng<span class="name-dot">.</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button>
<nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(nav)}<a class="cv-link" href="Chuiyang_Meng_CV.pdf" target="_blank" rel="noopener">CV ↗</a></nav></header>
<main class="container" id="main" tabindex="-1">{content}</main>
<footer class="site-footer container"><p>© <span id="year">2026</span> Chuiyang Meng</p><div><a href="mailto:chuiyang_meng@sfu.ca">Email</a><a href="https://github.com/chuiyangmeng96" target="_blank" rel="noopener">GitHub ↗</a><a href="Chuiyang_Meng_CV.pdf" target="_blank" rel="noopener">Curriculum vitae ↗</a></div></footer>
<dialog class="figure-dialog" aria-labelledby="preview-title"><button class="close-preview" type="button" aria-label="Close figure preview">×</button><div class="preview-body"></div></dialog>
</body></html>
'''


def heading(label, title, description):
    return f'<header class="page-heading"><p class="eyebrow">{label}</p><h1>{title}</h1><p>{description}</p></header>'


def row(date, place, organization, title, body):
    return f'''<article class="timeline-row"><p class="timeline-date">{date}<br><span>{place}</span></p>
    <div><p class="organization">{organization}</p><h3>{title}</h3>{body}</div></article>'''


def news_item(item):
    date_label = datetime.strptime(item["date"], "%Y-%m").strftime("%B %Y")
    return f'''<li class="news-item"><time datetime="{e(item['date'])}">{date_label}</time>
    <div><h3><a href="{e(item['href'])}">{e(item['title'])}</a></h3><p>{e(item['body'])}</p></div></li>'''


news = '<section class="news-section" id="news" aria-labelledby="news-title"><div class="section-heading"><h2 id="news-title">News</h2></div><ul class="news-list">'
news += "".join(news_item(item) for item in NEWS[:4]) + "</ul>"
if len(NEWS) > 4:
    news += f'<details class="news-archive"><summary>Earlier updates <span>({len(NEWS) - 4})</span></summary><ul class="news-list">'
    news += "".join(news_item(item) for item in NEWS[4:]) + "</ul></details>"
news += "</section>"


home = '''<section class="intro" aria-labelledby="intro-title"><div class="intro-copy">
  <p class="eyebrow">POSTDOCTORAL RESEARCH FELLOW · SIMON FRASER UNIVERSITY</p>
  <h1 id="intro-title">Chuiyang Meng</h1>
  <p class="intro-lead">I study how intelligent systems learn, reason, and collaborate, from the behavior of individual models to collective intelligence.</p>
  <p>I am a Postdoctoral Research Fellow at Simon Fraser University. I received my PhD in Electrical and Computer Engineering from the University of British Columbia in June 2026, advised by <a href="https://people.ece.ubc.ca/vincentw/">Prof. Vincent W.S. Wong</a>.</p>
  <p>My work connects foundation models and mechanistic interpretability with multi-agent systems, distributed learning, and communication networks.</p>
  <div class="intro-links" aria-label="Contact and profiles">
    <a class="social-link" href="mailto:chuiyang_meng@sfu.ca" aria-label="Email"><img src="assets/icons/email.svg" alt="" width="24" height="24" aria-hidden="true"></a>
    <a class="social-link" href="https://scholar.google.com/citations?user=MLB0NZsAAAAJ&amp;hl=zh-CN" target="_blank" rel="noopener" aria-label="Google Scholar"><img src="assets/icons/google-scholar.png" alt="" width="24" height="24" aria-hidden="true"></a>
    <a class="social-link" href="https://orcid.org/0009-0000-9381-4916" target="_blank" rel="noopener" aria-label="ORCID"><img src="assets/icons/orcid.svg" alt="" width="24" height="24" aria-hidden="true"></a>
    <a class="social-link" href="https://www.linkedin.com/in/chuiyang-meng-b54a48185" target="_blank" rel="noopener" aria-label="LinkedIn"><img src="assets/icons/linkedin.png" alt="" width="24" height="24" aria-hidden="true"></a>
    <a class="social-link" href="https://github.com/chuiyangmeng96" target="_blank" rel="noopener" aria-label="GitHub"><img src="assets/icons/github.svg" alt="" width="24" height="24" aria-hidden="true"></a>
    <a class="social-link social-link--cv" href="Chuiyang_Meng_CV.pdf" target="_blank" rel="noopener" aria-label="Curriculum vitae">CV</a>
  </div>
  </div><figure class="profile-photo"><img src="life-photo-1.jpg" alt="Chuiyang Meng" width="190" height="236" fetchpriority="high"></figure>
</section>
<section class="research-section" aria-labelledby="research-title"><div class="section-heading"><h2 id="research-title">Research interests</h2></div>
  <div class="research-grid">
    <article><span class="topic-number">01</span><h3>Foundation models</h3><p>Efficient adaptation and learning dynamics of large models.</p></article>
    <article><span class="topic-number">02</span><h3>Mechanistic interpretability</h3><p>Causal mechanisms and emerging specialization inside neural networks.</p></article>
    <article><span class="topic-number">03</span><h3>Multi-agent systems</h3><p>Communication, collective reasoning, and the spread of errors.</p></article>
    <article><span class="topic-number">04</span><h3>Distributed & edge learning</h3><p>Federated and split learning across heterogeneous devices.</p></article>
    <article><span class="topic-number">05</span><h3>Communications & networks</h3><p>Resource allocation and coordination in wireless networks.</p></article>
  </div>
</section>'''
home += news
home += '''<section class="selected-section" aria-labelledby="selected-title"><div class="section-heading"><h2 id="selected-title">Selected research</h2><a class="text-link" href="publications.html">All publications →</a></div>'''
home += "".join(paper(p) for p in PAPERS if p.get("featured"))
home += '''</section><div class="about-bottom">
  <section><h2>Experience & service</h2><p>My experience includes responsible AI research at the Vector Institute and teaching assistantships at UBC and Johns Hopkins.</p><div class="about-links"><a class="text-link" href="experience.html">Experience & education →</a><a class="text-link" href="teaching.html">Teaching & service →</a></div></section>
  <section><h2>Get in touch</h2><p>For research discussions and collaboration, please reach out by email.</p><a class="email-link" href="mailto:chuiyang_meng@sfu.ca">chuiyang_meng@sfu.ca</a></section>
</div>'''

publications = heading("RESEARCH", "Publications", "Papers and manuscripts on mechanistic interpretability, distributed intelligence, and wireless systems.")
publications += '''<div class="publication-controls" hidden><div class="publication-toolbar">
  <div class="selection-control" role="group" aria-label="Publication selection"><button type="button" data-selection="selected" aria-pressed="false">Selected</button><button type="button" data-selection="all" aria-pressed="true">All papers</button></div>
  <p class="author-note">My name is shown in <strong>bold</strong>.</p></div>
  <div class="topic-filters" role="group" aria-label="Filter by research topic"><button type="button" data-topic-filter="all" aria-pressed="true">All topics</button><button type="button" data-topic-filter="interpretability" aria-pressed="false">Mechanistic interpretability</button><button type="button" data-topic-filter="federated" aria-pressed="false">Federated & distributed learning</button><button type="button" data-topic-filter="wireless" aria-pressed="false">Wireless communications</button></div>
</div><div id="publication-list">'''
for year in sorted({p["year"] for p in PAPERS}, reverse=True):
    publications += f'<section class="publication-year" aria-labelledby="year-{year}"><h2 class="year-label" id="year-{year}">{year}</h2>'
    publications += "".join(paper(p) for p in PAPERS if p["year"] == year) + "</section>"
publications += '''</div><p class="no-results" hidden>No papers match these filters. <button class="reset-filters" type="button">Show all papers</button></p><p class="publication-status" role="status" aria-live="polite" hidden></p>'''

skills = '''<div class="skills-grid"><div><h3>Programming & tools</h3><p>Python, PyTorch, MATLAB, Linux, GitHub, Hugging Face, LaTeX</p></div><div><h3>Methods</h3><p>Distributed machine learning, mathematical optimization, resource allocation</p></div><div><h3>Languages</h3><p>English · Proficient<br>Mandarin Chinese · Native</p></div></div>'''
background = heading("BACKGROUND", "Experience & education", "Research at the intersection of machine learning, communications, and networked systems.")
background += '''<nav class="page-index" aria-label="On this page"><a href="#experience">Experience</a><a href="#education">Education</a><a href="#awards">Awards</a><a href="#skills">Skills</a></nav><section class="content-section" id="experience"><h2>Experience</h2>'''
background += row("Sep 2026 – Present", "Coquitlam, Canada", "Simon Fraser University", "Postdoctoral Research Fellow", "")
background += row("Jan 2026 – Apr 2026", "Toronto, Canada", "Vector Institute · Responsible AI Team", "Applied Machine Learning Intern", '<p class="muted">Deepfake video detection and robust machine learning.</p><ul><li>Developed training and validation pipelines for deepfake video detection.</li><li>Worked on robustness in real-world forgery scenarios.</li></ul>')
background += row("Sep 2021 – Jun 2026", "Vancouver, Canada", "University of British Columbia", "Graduate Research Assistant", '<p class="muted">Advisor: Prof. Vincent W.S. Wong</p><ul><li>Resource-efficient federated fine-tuning through low-rank and zeroth-order optimization.</li><li>Adaptive split learning and graph-based resource allocation for decentralized learning.</li><li>Learning dynamics and emergent modularity in foundation models.</li></ul>')
background += '</section><section class="content-section" id="education"><h2>Education</h2>'
background += row("Sep 2021 – Jun 2026", "Vancouver, Canada", "University of British Columbia", "PhD in Electrical and Computer Engineering", '<p class="muted">Thesis: Resource-aware Distributed Edge Intelligence</p><p class="muted">Advisor: Prof. Vincent W.S. Wong</p>')
background += row("Aug 2018 – May 2020", "Baltimore, USA", "Johns Hopkins University", "MS in Electrical and Computer Engineering", "")
background += row("Sep 2014 – Jun 2018", "Harbin, China", "Harbin Institute of Technology", "BEng in Electronics and Information Engineering", '<p class="muted">Advisors: Prof. Shuai Han and Prof. Hsiao-Hwa Chen</p>')
background += '''</section><section class="content-section" id="awards"><h2>Awards</h2><ul class="service-list">
  <li><strong>IEEE INFOCOM Student Travel Grant</strong><p class="muted">2026 · US$1,640</p></li>
  <li><strong>President’s Academic Excellence Initiative PhD Award</strong><p class="muted">University of British Columbia · 2021–2026</p></li>
  <li><strong>International Tuition Award</strong><p class="muted">University of British Columbia · 2021–2026</p></li>
</ul>'''
background += f'</section><section class="content-section" id="skills"><h2>Skills</h2>{skills}<p class="membership">IEEE Member</p></section>'

teaching = heading("ACADEMIC COMMUNITY", "Talks, teaching & service", "Sharing research, supporting students, and contributing to the research community.")
teaching += '<section class="content-section" id="talks" aria-labelledby="talks-title"><h2 id="talks-title">Talks</h2>'
for talk in TALKS:
    date_label = datetime.strptime(talk["date"], "%Y-%m-%d").strftime("%B %d, %Y")
    teaching += f'''<article class="timeline-row" id="{e(talk['id'])}">
    <p class="timeline-date"><time datetime="{e(talk['date'])}">{date_label}</time><br><span>{e(talk['location'])}</span></p>
    <div><p class="organization">{e(talk['event'])}</p><h3>{e(talk['title'])}</h3>
    <p class="muted">{e(talk['institution'])} · {e(talk['status'])}</p>
    <a class="text-link" href="{e(talk['eventUrl'])}">Workshop details →</a></div></article>'''
teaching += '</section>'
teaching += '<section class="content-section"><h2>Teaching</h2>'
teaching += row("2021–2025", "Vancouver, Canada", "University of British Columbia", "ELEC 331 · Computer Communications", '<p class="muted">Teaching Assistant</p><p>Fall 2021, Spring 2022, Fall 2023, Spring 2024, Spring 2025</p>')
teaching += row("Fall 2019", "Baltimore, USA", "Johns Hopkins University", "EN.520.647 · Information Theory", '<p class="muted">Teaching Assistant</p>')
teaching += '''</section><section class="content-section"><h2>Conference service</h2><h3>Technical Program Committee (TPC) Symposium Chair</h3><p class="muted">International Conference on Wireless Communications and Signal Processing (WCSP) · Shenzhen, China</p></section><section class="content-section"><h2>Peer review</h2><ul class="service-list"><li>Conference on Neural Information Processing Systems (NeurIPS)</li><li>IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</li><li>International Conference on Learning Representations (ICLR)</li><li>IEEE Transactions on Wireless Communications</li><li>IEEE Transactions on Mobile Computing</li><li>IEEE Transactions on Communications</li><li>IEEE Internet of Things Journal</li><li>IEEE Wireless Communications Magazine</li></ul></section>'''

outputs = {
    "index.html": ("About", "about", "Chuiyang Meng — Postdoctoral Research Fellow at Simon Fraser University. Research in foundation models, mechanistic interpretability, multi-agent systems, distributed learning, and communication networks.", home),
    "publications.html": ("Publications", "publications", "Research publications by Chuiyang Meng, with paper PDFs, method figures, and citations.", publications),
    "experience.html": ("Background", "background", "Chuiyang Meng's research experience, education, and technical background.", background),
    "teaching.html": ("Talks, teaching & service", "teaching", "Research talks, teaching, and academic service by Chuiyang Meng.", teaching),
    "skills.html": ("Skills", "background", "Chuiyang Meng's technical skills and methods.", heading("BACKGROUND", "Skills", 'See my full <a href="experience.html">experience and education →</a>') + '<section class="content-section">' + skills + '</section>'),
}
for filename, args in outputs.items():
    (ROOT / filename).write_text(page(*args, filename=filename), encoding="utf-8")
sitemap_urls = [canonical_url(filename) for filename in outputs if filename != "skills.html"]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "".join(f"  <url><loc>{e(url)}</loc></url>\n" for url in sitemap_urls)
sitemap += "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
print(f"Built {len(outputs)} pages with {len(PAPERS)} publications.")
