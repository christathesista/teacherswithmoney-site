# teacherswithmoney.com: site files

Built October 12, 2026 in the Teachers With Money project chat. Copy = "Website Page Copy v2" (Google Doc in this folder), with the beehiiv form details from the beehiiv launch chat.

## What's here

- `site/`: the finished website. This is what gets deployed.
  - `index.html`: the homepage. The two beehiiv signup forms are live embeds.
  - `privacy.html`: the privacy policy page.
  - `assets/`: images (coin apple, headshot, podcast cover, share image, browser-tab icons).
- `src/` + `build.py`: the source the site is generated from. To change copy, edit `src/index-main.html` (or `src/privacy-main.html`), then run `python3 build.py` to regenerate `site/`.

## Rules baked into the page (from Christa, Oct 8)

- Summit wording is "late January" only. No dates, no year, no countdown.
- No Teachers Pay Teachers seller tiers, tier names, or payout numbers anywhere.
- TPT Launch Lab is a plain footer link only. No description copy.
- Newsletter signup is the main button, the podcast is second.
- Copy talks to teachers. Nothing sold to sellers, no "work with me."
- Coaching stays a footer link (Christa is still deciding about it).

## Before launch (must do)

1. **Effective date** in `src/privacy-main.html` is "ADD ON LAUNCH DAY". Set it in `build.py` (search `ADD ON LAUNCH DAY`) to the real launch date and rebuild.
2. **Test both signup forms yourself** on the live site with a personal email. beehiiv shows a "press and hold" bot check that Claude can't complete.
3. **Third episode card** is EP2 as a stand-in. Swap it if Christa picks a different one.
4. **Confirm the TPT Launch Lab Samcart link still works.** Claude couldn't open it to check (unverified).

## Deploying (GitHub Pages, recommended)

GitHub Pages is free, gives HTTPS, and works with the domain where it already lives (Squarespace Domains), so the nameservers don't move.

DNS rules for teacherswithmoney.com:
- ADD only the website records GitHub gives you (A records for the root domain, a CNAME for `www`).
- DO NOT touch the existing mail records: the Google Workspace MX records, the SPF TXT record (`v=spf1 include:_spf.google.com ~all`), the DMARC record (`_dmarc`), or the Google site-verification TXT. Changing any of them can break Christa's email.

## No analytics

The site has no analytics or ad tracking on purpose. The privacy policy says so. If analytics ever get added, update the privacy policy first.
