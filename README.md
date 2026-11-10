# Chuiyang Meng — Personal Website

A static academic website with a publication list, paper PDFs, and expandable research figures. The layout takes inspiration from the clarity and organization of [Yue Yang's homepage](https://yy-gx.github.io/publications/), with original implementation and right-aligned paper figures.

## Preview locally

```sh
python3 scripts/build_site.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [the homepage](http://127.0.0.1:8765/) or [publications](http://127.0.0.1:8765/publications.html).

The checked-in HTML works directly on GitHub Pages. Python is only needed when regenerating it; no frontend dependencies or build service are required.

## Edit content

- `data/publications.json`: the source for all ten paper records. Set `featured` to choose the five homepage papers and `selected` for the optional publications-page selection. `summary` appears in the list; `explanation` appears beside the enlarged figure. Submitted manuscripts use `type: "preprint"` with an explicit `status`. An `arxivId` adds `eprint` and `archivePrefix` to a `misc` BibTeX entry; manuscripts without an arXiv ID export as `unpublished`. Structured `volume` and `number` fields are included in journal citations. Acceptance rates for FLoRG (27%) and ZorBA (18%) are user-provided values.
- `data/news.json`: dated updates, sorted newest first. The homepage shows four entries and a native disclosure for earlier updates. Dates and provenance are recorded per entry; FLoRG (January 2026), ZorBA (December 2025), and ASFL (June 2026) acceptance months were confirmed by the user. The news format follows the dated, short-headline style of [Yue Yang's About page](https://yy-gx.github.io/about/).
- `scripts/build_site.py`: shared HTML templates, biography, research interests, education, experience, and teaching. Run it after changing content.
- `data/talks.json`: research talks with exact dates, event links, venues, and status. These appear in the Talks section of `teaching.html`; update the status after a scheduled talk takes place. The November 11, 2026 talk follows the current academic CV, with the official workshop name verified as IEEE MWN.
- `styles.css`: layout, colors, spacing, and responsive styles.
- `script.js`: topic/selection filters, native image dialog, navigation menu, and citation copying.
- `assets/papers/`: author-hosted paper PDFs.
- `assets/figures/`: original-resolution figure extracts and lightweight WebP thumbnails.
- `assets/icons/`: official profile icons and a generic email icon, with sources in its README. CV remains text; the ORCID link was supplied by the user.

For a new paper, add its record and assets, then regenerate the HTML. Optional `arxiv` and `doi` fields add external resource links. Missing assets are omitted rather than replaced with broken buttons or invented images.

The five pages are About (`index.html`), Publications, Background (`experience.html`), Teaching & service, and a retained `skills.html` page for existing links. Publications opens with all ten papers; choosing a topic searches the complete list. Without JavaScript, the complete paper list and direct full-size image links still work. On phones, paper figures move below the text. On narrow screens, citation panels stay within the viewport.

## Recovered content and asset provenance

The original public repository and history were recovered from `chuiyangmeng96/chuiyangmeng96.github.io`. The photograph comes from that recovered site. Biography, contact details, experience, education, awards, and academic service were synchronized with the author's current CV on September 27, 2026. The downloadable CV was refreshed on November 10, 2026 from `output/pdf/academic_cv/Chuiyang_Meng_CV.tex`, including the November 11 workshop talk, using the embedded original class. The workshop abbreviation was corrected to the official MWN spelling. CV links include a content hash so new releases bypass cached copies; the permanent PDF path remains unchanged.

Social Circuits and CORTEX link to their public arXiv records, [2609.34444](https://arxiv.org/abs/2609.34444) and [2609.34449](https://arxiv.org/abs/2609.34449). Their PDF buttons use the corresponding arXiv PDF URLs so readers receive the latest public versions. Titles, authors, identifiers, and submission dates were verified against the official arXiv API. The existing figures were extracted from author manuscripts prepared on September 27, 2026. Both papers retain their submitted-to-ICLR-2027 status; arXiv availability does not imply conference acceptance.

The five recent PDFs were retrieved from [Vincent W.S. Wong's UBC publication page](https://people.ece.ubc.ca/vincentw/Homepage/Publication.html). Exact PDF URLs and figure page numbers are recorded per publication in `data/publications.json`. Figures are cropped from the papers themselves. ASFL's venue/year was updated to IEEE TMC 2026 based on that public listing.

The three 2017 papers currently have DOI/publisher links and citations. Author PDFs and suitable figures were not recovered; these remain to be supplied. No placeholder PDF links are shown.

## Publishing

The public site is [chuiyangmeng96.github.io](https://chuiyangmeng96.github.io/). Pushing to `main` triggers GitHub Pages deployment. The workflow stages only public website files in `_site/` before uploading the artifact.

The build generates canonical URLs, profile structured data, `robots.txt`, and a four-page sitemap for search discovery. Search engines decide when to crawl and index updates. The existing Homepage link in the CV points to this same permanent address.
