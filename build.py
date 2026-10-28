"""Build the Teachers With Money site (site/) and the private preview (preview/).

site/     = the real files to deploy: beehiiv embeds live, full HTML documents.
preview/  = the same page for a Claude artifact preview: no doctype wrapper on the
            main page, beehiiv embeds swapped for look-alike stand-ins (the preview
            sandbox can't load beehiiv's script).
"""
import pathlib, shutil, sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
SITE = ROOT / "site"
PREVIEW = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "preview"

css = (SRC / "styles.css").read_text()
header = (SRC / "header.html").read_text()
footer = (SRC / "footer.html").read_text()
index_main = (SRC / "index-main.html").read_text()
privacy_main = (SRC / "privacy-main.html").read_text()
pillars_main = (SRC / "pillars-main.html").read_text()
partners_main = (SRC / "partners-main.html").read_text()
media_kit = (SRC / "media-kit.html").read_text()
summit_main = (SRC / "summit-main.html").read_text()
summit_thanks_main = (SRC / "summit-thanks-main.html").read_text()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,400..900,0..100;1,9..144,400..900,0..100&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Shrikhand&display=swap">')

TITLE = "Teachers With Money | Real money talk for educators"
DESC = ("Real money talk for educators, with zero guilt. A podcast every Tuesday, a "
        "newsletter every Wednesday, and a free online summit on January 30 and 31, 2027.")

def embed(form_id):
    return ('<script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" '
            f'data-beehiiv-form="{form_id}"></script>')

NEWSLETTER_ID = "b6cd0344-203d-4142-9f4f-25e7c0bf6114"
SUMMIT_ID = "04d15350-3e84-45c0-912f-db1615eafa2d"
ATTRIBUTION = '<script type="text/javascript" async src="https://subscribe-forms.beehiiv.com/attribution.js"></script>'
CONFETTI_JS = (ROOT / "src" / "confetti.js").read_text()
REDIRECT_JS = (ROOT / "src" / "redirect-newtab.js").read_text()

def stub(button):
    return ('<div class="embed-stub" role="img" aria-label="Preview of the beehiiv signup form">'
            '<span class="field">personal email (not school!)</span>'
            f'<span class="btn btn--primary">{button}</span></div>'
            '<p class="embed-stub-note">PREVIEW ONLY: the live beehiiv form loads here on teacherswithmoney.com</p>')

def head(title, desc, canonical, extra=""):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Teachers With Money">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://teacherswithmoney.com/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#315647">
<link rel="icon" type="image/png" href="assets/favicon-64.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{FONTS}
<style>
{css}</style>{extra}"""

def page(head_html, body_html):
    return f"<!doctype html>\n<html lang=\"en\">\n<head>\n{head_html}\n</head>\n<body>\n{body_html}\n</body>\n</html>\n"

# ---------- real site ----------
if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
shutil.copytree(ROOT / "assets", SITE / "assets")

idx_body = (header.replace("{{HOME}}", "") +
            index_main.replace("{{FORM_NEWSLETTER}}", embed(NEWSLETTER_ID))
                      .replace("{{FORM_SUMMIT}}", embed(SUMMIT_ID)).replace("{{CONFETTI_JS}}", CONFETTI_JS).replace("{{REDIRECT_JS}}", REDIRECT_JS) +
            footer.replace("{{HOME}}", "") + ATTRIBUTION)
(SITE / "index.html").write_text(page(head(TITLE, DESC, "https://teacherswithmoney.com/"), idx_body))

priv_body = (header.replace("{{HOME}}", "/") +
             privacy_main.replace("{{EFFECTIVE_DATE}}", "October 14, 2026") +
             footer.replace("{{HOME}}", "/"))
(SITE / "privacy.html").write_text(page(
    head("Privacy Policy | Teachers With Money",
         "How Teachers With Money handles the email address you share with us.",
         "https://teacherswithmoney.com/privacy.html"), priv_body))

PILLARS_TITLE = "Our Pillars | Teachers With Money"
PILLARS_DESC = ("The five pillars behind Teachers With Money: side hustles, wealth strategy, "
                "money and mental health, teacher pathways, and systemic change.")
pillars_body = header.replace("{{HOME}}", "/") + pillars_main + footer.replace("{{HOME}}", "/")
(SITE / "pillars.html").write_text(page(
    head(PILLARS_TITLE, PILLARS_DESC, "https://teacherswithmoney.com/pillars.html"), pillars_body))

# Optional partner-page lines Christa has not approved yet stay empty until she says so.
PARTNER_RULES = "<p>I don't work with MLMs or predatory lenders.</p>"
ABOUT_EXTRAS = ""    # Adobe MAX mention left off on purpose (Oct 16): it would go stale fast; LinkedIn carries it.
PARTNERS_TITLE = "Partner with Teachers With Money | Christa Jones"
PARTNERS_DESC = ("Sponsorships, creator partnerships, podcast collaborations, and speaking with Christa Jones, "
                 "founder of Teachers With Money and host of First in Class.")
partners_body = (header.replace("{{HOME}}", "/") +
                 partners_main.replace("{{PARTNER_RULES}}", PARTNER_RULES).replace("{{ABOUT_EXTRAS}}", ABOUT_EXTRAS) +
                 footer.replace("{{HOME}}", "/"))
(SITE / "partners.html").write_text(page(
    head(PARTNERS_TITLE, PARTNERS_DESC, "https://teacherswithmoney.com/partners.html"), partners_body))
(SITE / "media-kit.html").write_text(media_kit.replace("{{FONTS}}", FONTS).replace("{{CSS}}", css))

# media-kit.pdf: print the one-page kit with headless Chrome, when Chrome is installed.
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if pathlib.Path(CHROME).exists():
    import subprocess
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={SITE / 'media-kit.pdf'}",
                    (SITE / "media-kit.html").resolve().as_uri()],
                   check=True, capture_output=True)
else:
    print("WARNING: Chrome not found, media-kit.pdf not regenerated")

(SITE / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>https://teacherswithmoney.com/{p}</loc></url>\n" for p in ("", "summit/", "pillars.html", "partners.html", "privacy.html")) +
    "</urlset>\n")
(SITE / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /media-kit.html\nDisallow: /summit/thanks/\nSitemap: https://teacherswithmoney.com/sitemap.xml\n")

# ---------- Summit pages (/summit/ and /summit/thanks/) ----------
# THE SUMMIT FORM. Today: the "Summit waitlist - website" beehiiv form (same as the homepage).
# Dec 28, 2026: paste the "Summit registration - website" form ID here. One line, then rebuild.
SUMMIT_PAGE_FORM_ID = SUMMIT_ID

import json
def nested(html):
    """Root-relative asset and page links for pages that live one folder down."""
    for a in ('src="assets/', 'srcset="assets/', 'href="assets/'):
        html = html.replace(a, a.replace('"assets/', '"/assets/'))
    for page in ("privacy.html", "pillars.html", "partners.html", "media-kit.pdf"):
        html = html.replace(f'href="{page}"', f'href="/{page}"')
    return html

def speakers_html():
    """The lineup as an album tracklist: Side A (Day 1) and Side B (Day 2), liner notes per track."""
    speakers = json.loads((ROOT / "data" / "speakers.json").read_text())
    def side_of(s):
        side = str(s.get("side", "")).upper()
        if side in ("A", "B"): return side
        return "B" if str(s.get("day", "")) == "2" else "A"
    def track(i, s):
        links = "".join(f'<a href="{l["url"]}" target="_blank" rel="noopener">{l["label"]}</a>' for l in s.get("links", []))
        links = f'<p class="small links">{links}</p>' if links else ""
        photo = f'<img src="/{s["photo"]}" alt="{s["name"]}" width="320" height="320" loading="lazy">' if s.get("photo") else ""
        bio = f'<p>{s["bio"]}</p>' if s.get("bio") else ""
        return ('<li class="track"><details><summary>'
                f'<span class="num">{i:02d}</span><span class="title">{s.get("session", "")}</span><span class="artist">{s["name"]}</span>'
                f'</summary><div class="liner">{photo}<div class="stack"><p class="eyebrow tiny">liner notes</p>{bio}{links}</div></div></details></li>')
    def blank(i):
        return f'<li class="track blank"><span class="num">{i:02d}</span><span class="title"></span><span class="artist">announcing in january</span></li>'
    def side(letter, label, items):
        tracks = "".join(track(i, s) for i, s in enumerate(items, 1)) if items else "".join(blank(i) for i in range(1, 5))
        return f'<div class="side"><p class="eyebrow small">side {letter.lower()} · {label}</p><ol class="tracks">{tracks}</ol></div>'
    a = [s for s in speakers if side_of(s) == "A"]
    bb = [s for s in speakers if side_of(s) == "B"]
    if speakers:
        head = '<h2 id="speakers-title">The tracklist.</h2>'
    else:
        head = ('<h2 id="speakers-title">The tracklist drops in January.</h2><!-- DRAFT COPY: Christa to review -->\n'
                '        <p class="lead">Waitlist hears the names first.</p><!-- DRAFT COPY: Christa to review -->')
    return (head + '\n        <div class="tracklist">' + side("A", "saturday, january 30", a) + side("B", "sunday, january 31", bb) + '</div>')

SUMMIT_TITLE = "Teachers With Money Summit | Free, Jan 30\u201331, 2027"
SUMMIT_DESC = "A free weekend of teacher money basics, without the overwhelm. January 30 and 31, 2027, online."
summit_header = header.replace("{{HOME}}", "/").replace('<a href="/#summit">Summit</a>', '<a href="#top" aria-current="page">Summit</a>')
summit_body = (summit_header +
               summit_main.replace("{{FORM_SUMMIT_PAGE}}", embed(SUMMIT_PAGE_FORM_ID)).replace("{{SPEAKERS}}", speakers_html()).replace("{{CONFETTI_JS}}", CONFETTI_JS).replace("{{REDIRECT_JS}}", REDIRECT_JS) +
               footer.replace("{{HOME}}", "/") + ATTRIBUTION)
(SITE / "summit").mkdir(exist_ok=True)
(SITE / "summit" / "index.html").write_text(nested(page(
    head(SUMMIT_TITLE, SUMMIT_DESC, "https://teacherswithmoney.com/summit/"), summit_body)))

thanks_body = summit_header + summit_thanks_main.replace("{{CONFETTI_JS}}", CONFETTI_JS) + footer.replace("{{HOME}}", "/")
(SITE / "summit" / "thanks").mkdir(exist_ok=True)
(SITE / "summit" / "thanks" / "index.html").write_text(nested(page(
    head("You're in! | Teachers With Money Summit", "You're on the list for the Teachers With Money Summit, January 30 and 31, 2027.",
         "https://teacherswithmoney.com/summit/thanks/", extra='\n<meta name="robots" content="noindex">'), thanks_body)))

def ics(uid, summary, start, end, desc):
    return ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Teachers With Money//Summit//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n"
            f"BEGIN:VEVENT\r\nUID:{uid}@teacherswithmoney.com\r\nDTSTAMP:20261026T120000Z\r\nDTSTART;VALUE=DATE:{start}\r\nDTEND;VALUE=DATE:{end}\r\n"
            f"SUMMARY:{summary}\r\nDESCRIPTION:{desc}\r\nLOCATION:Online\r\nURL:https://teacherswithmoney.com/summit/\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
(SITE / "summit" / "twm-summit-day-1.ics").write_text(ics("twm-summit-2027-day1", "Teachers With Money Summit, Day 1", "20270130", "20270131",
    "Day 1: getting your money right. Free and online. https://teacherswithmoney.com/summit/"))
(SITE / "summit" / "twm-summit-day-2.ics").write_text(ics("twm-summit-2027-day2", "Teachers With Money Summit, Day 2", "20270131", "20270201",
    "Day 2: growing income around the pay scale. Free and online. https://teacherswithmoney.com/summit/"))

# ---------- preview ----------
if PREVIEW.exists():
    shutil.rmtree(PREVIEW)
PREVIEW.mkdir(parents=True)
shutil.copytree(ROOT / "assets", PREVIEW / "assets")
prev_main = (f"<title>Teachers With Money</title>\n{FONTS}\n<style>\n{css}</style>\n" +
             header.replace("{{HOME}}", "") +
             index_main.replace("{{FORM_NEWSLETTER}}", stub("Count me in"))
                       .replace("{{FORM_SUMMIT}}", stub("Save my spot")).replace("{{CONFETTI_JS}}", CONFETTI_JS).replace("{{REDIRECT_JS}}", REDIRECT_JS) +
             footer.replace("{{HOME}}", ""))
(PREVIEW / "index.html").write_text(prev_main)
(PREVIEW / "privacy.html").write_text(page(
    head("Privacy Policy", "Privacy policy preview", "https://teacherswithmoney.com/privacy.html"),
    header.replace("{{HOME}}", "./") +
    privacy_main.replace("{{EFFECTIVE_DATE}}", "October 14, 2026") +
    footer.replace("{{HOME}}", "./")))
(PREVIEW / "pillars.html").write_text(page(
    head(PILLARS_TITLE, PILLARS_DESC, "https://teacherswithmoney.com/pillars.html"),
    header.replace("{{HOME}}", "./") + pillars_main + footer.replace("{{HOME}}", "./")))
print("built", SITE, PREVIEW)
