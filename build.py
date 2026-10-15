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

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,400..900,0..100;1,9..144,400..900,0..100&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Sacramento&display=swap">')

TITLE = "Teachers With Money | Real money talk for educators"
DESC = ("Real money talk for educators, with zero guilt. A podcast every Tuesday, a "
        "newsletter every Wednesday, and a free online summit in late January.")

def embed(form_id):
    return ('<script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" '
            f'data-beehiiv-form="{form_id}"></script>')

NEWSLETTER_ID = "b6cd0344-203d-4142-9f4f-25e7c0bf6114"
SUMMIT_ID = "04d15350-3e84-45c0-912f-db1615eafa2d"
ATTRIBUTION = '<script type="text/javascript" async src="https://subscribe-forms.beehiiv.com/attribution.js"></script>'

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
                      .replace("{{FORM_SUMMIT}}", embed(SUMMIT_ID)) +
            footer.replace("{{HOME}}", "") + ATTRIBUTION)
(SITE / "index.html").write_text(page(head(TITLE, DESC, "https://teacherswithmoney.com/"), idx_body))

priv_body = (header.replace("{{HOME}}", "/") +
             privacy_main.replace("{{EFFECTIVE_DATE}}", "October 14, 2026") +
             footer.replace("{{HOME}}", "/"))
(SITE / "privacy.html").write_text(page(
    head("Privacy Policy | Teachers With Money",
         "How Teachers With Money handles the email address you share with us.",
         "https://teacherswithmoney.com/privacy.html"), priv_body))

# ---------- preview ----------
if PREVIEW.exists():
    shutil.rmtree(PREVIEW)
PREVIEW.mkdir(parents=True)
shutil.copytree(ROOT / "assets", PREVIEW / "assets")
prev_main = (f"<title>Teachers With Money</title>\n{FONTS}\n<style>\n{css}</style>\n" +
             header.replace("{{HOME}}", "") +
             index_main.replace("{{FORM_NEWSLETTER}}", stub("Count me in"))
                       .replace("{{FORM_SUMMIT}}", stub("Save my spot")) +
             footer.replace("{{HOME}}", ""))
(PREVIEW / "index.html").write_text(prev_main)
(PREVIEW / "privacy.html").write_text(page(
    head("Privacy Policy", "Privacy policy preview", "https://teacherswithmoney.com/privacy.html"),
    header.replace("{{HOME}}", "./") +
    privacy_main.replace("{{EFFECTIVE_DATE}}", "October 14, 2026") +
    footer.replace("{{HOME}}", "./")))
print("built", SITE, PREVIEW)
