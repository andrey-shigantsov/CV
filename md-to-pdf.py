#!/usr/bin/env python3
"""
md-to-pdf.py — Convert CV markdown files to PDFs.

Pure-Python pipeline (no Node.js, no headless browser):
  markdown  — parses the markdown source to HTML (Python-Markdown).
  weasyprint — renders that HTML + cv-style.css to a PDF.

Reads every ``*.md`` file in this script's directory that carries a YAML
front-matter block with an ``updated`` field (ISO 8601), and renders each to
PDF in ``./pdf/<basename>.pdf`` (a single, overwritten file — no version
history). The front-matter date is injected into the body's ``{{DATE}}``
placeholder (e.g. the NOTE callout) so the displayed date stays in sync with
the edit timestamp.

Files without a front-matter ``updated`` field (e.g. ``AGENTS.md``) are skipped.

Requirements:
  - Python-Markdown  (pip install markdown  /  pacman -S python-markdown)
  - WeasyPrint       (pip install weasyprint / pacman -S python-weasyprint)
    WeasyPrint needs the system libs pango, cairo, gdk-pixbuf, libffi —
    `pacman -S python-weasyprint` pulls them in.
  - PyYAML (for reading the front-matter timestamp).
  - The stylesheet `cv-style.css` next to this script.

Usage:
    python3 md-to-pdf.py                # convert all eligible *.md
    python3 md-to-pdf.py file.md [...]  # convert specific file(s)
"""

import os
import re
import sys
import glob

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
STYLESHEET = os.path.join(HERE, "cv-style.css")

# Python-Markdown extensions we enable. `extra` bundles tables, fenced_code,
# footnotes, etc.; `attr_list`/`md_in_html` help with edge cases.
MD_EXTENSIONS = ["extra", "sane_lists", "attr_list"]

# NOTE callout text, by language. Injected at the top of every generated PDF
# (NOT kept in the markdown sources). Placeholders filled at render time:
#   {date}          — ISO date (YYYY-MM-DD) from the `updated` front-matter field.
#   {pdf_url}       — full direct URL to THIS file's PDF on GitHub (click target).
#   {pdf_url_short} — same URL without the "https://" scheme (visible text).
# To change the wording, edit it here.
CV_REPO_URL = "https://github.com/andrey-shigantsov/CV"
NOTE_TEXT = {
    # basename suffix → NOTE markdown (date on line 1, link on line 2 so the
    # URL gets its own line). The visible text is the URL WITHOUT the "https://"
    # scheme (for brevity); the clickable target is the full URL.
    # The two trailing spaces after the date line are a markdown hard line
    # break (<br>) — a single newline would render as a space.
    "English": "> ***NOTE***: *updated {date}*  \n"
               "> Latest version: [{pdf_url_short}]({pdf_url})",
    "Russian": "> ***NOTE***: *обновлено {date}*  \n"
               "> Актуальная версия: [{pdf_url_short}]({pdf_url})",
}


# --------------------------------------------------------------------------
# Front-matter
# --------------------------------------------------------------------------

def split_front_matter(text: str):
    """Return (meta_dict, body_text). meta is {} if no front-matter."""
    if not text.startswith("---"):
        return {}, text
    end = re.search(r"\n---\s*\n", text)
    if not end:
        return {}, text
    block = text[3:end.start()]
    body = text[end.end():]
    try:
        meta = yaml.safe_load(block) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), body


def _iso_date(meta: dict) -> str:
    """
    ISO 8601 calendar date (``YYYY-MM-DD``) from the ``updated`` front-matter
    field, or ``''`` if absent. Used to inject the date into the NOTE callout's
    ``{{DATE}}`` placeholder so it stays in sync with the edit timestamp.
    """
    updated = meta.get("updated")
    if not updated:
        return ""
    s = str(updated).strip()
    m = re.match(r"(\d{4})\D?(\d{2})\D?(\d{2})", s)
    if not m:
        return ""
    return "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_md_to_pdf(md_path: str, out_dir: str, meta: dict) -> str:
    """
    Render one markdown file to PDF via Python-Markdown + WeasyPrint, writing
    to <out_dir>/<basename>.pdf (a single, overwritten file — no history).
    A NOTE callout with the front-matter date (link to the latest version on
    GitHub) is generated and injected at the top of the document. The NOTE
    text itself lives in this script (NOT in the markdown), so the markdown
    stays clean. Returns the PDF path.
    """
    import markdown  # imported lazily so --help works without the dep
    from weasyprint import HTML

    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    _, body = split_front_matter(text)

    base = os.path.splitext(os.path.basename(md_path))[0]
    final_name = "%s.pdf" % base
    final_path = os.path.join(out_dir, final_name)

    # Markdown → HTML. The document title (H1) doubles as the PDF <title>.
    html_body = markdown.markdown(body, extensions=MD_EXTENSIONS)

    # Force the recommendations section onto a fresh page: add class
    # "recommendations" to its <h2> so cv-style.css can apply
    # `break-before: page`. Matches both language headings (RECOMENDATIONS /
    # РЕКОМЕНДАЦИИ), case-insensitive, whether or not the tag already has
    # attributes.
    def _tag_recommendations(m):
        attrs = m.group("attrs") or ""
        text = m.group("text")
        if "class=" in attrs:
            # append to an existing class list
            attrs = re.sub(r'class="([^"]*)"', r'class="\1 recommendations"',
                           attrs)
        else:
            attrs = (attrs + ' class="recommendations"').strip()
        return "<h2%s>%s</h2>" % (attrs and " " + attrs, text)

    html_body = re.sub(
        r"<h2(?P<attrs>\s[^>]*)?>(?P<text>\s*(?:RECOMENDATIONS|РЕКОМЕНДАЦИИ)\s*)</h2>",
        _tag_recommendations, html_body, flags=re.IGNORECASE,
    )

    # Generate the NOTE callout (date + link) and inject it at the top of the
    # body, before the H1. The NOTE text is NOT in the markdown; it lives in
    # NOTE_TEXT above so the markdown sources stay clean.
    lang_key = "Russian" if base.endswith("_Russian") else "English"
    # Direct link to THIS file's PDF on GitHub (full file name). `raw/` serves
    # the binary directly; `blob/` shows the GitHub preview page.
    pdf_url = "%s/raw/main/pdf/%s.pdf" % (CV_REPO_URL, base)
    # Visible link text = URL without the "https://" scheme, for brevity.
    pdf_url_short = re.sub(r"^https?://", "", pdf_url)
    note_md = NOTE_TEXT[lang_key].format(
        date=_iso_date(meta), pdf_url=pdf_url, pdf_url_short=pdf_url_short)
    note_html = markdown.markdown(note_md, extensions=MD_EXTENSIONS)
    html_body = note_html + "\n" + html_body

    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    title = (title_match.group(1).strip() if title_match else base)
    # crude tag strip for <title>
    title = re.sub(r"<[^>]+>", "", title)

    html_doc = """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<link rel="stylesheet" href="%(css)s">
</head>
<body>
%(body)s
</body>
</html>
""" % {
        "lang": "ru" if base.endswith("_Russian") else "en",
        "title": title,
        "css": STYLESHEET,
        "body": html_body,
    }

    # base_url lets WeasyPrint resolve relative asset paths
    # (./Recomendations/...) against the markdown source directory.
    HTML(string=html_doc, base_url=os.path.dirname(os.path.abspath(md_path))
         ).write_pdf(final_path)

    print("OK   %s -> %s" % (os.path.basename(md_path), final_name))
    return final_path


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv):
    if not os.path.exists(STYLESHEET):
        sys.exit("ERROR: stylesheet not found: %s" % STYLESHEET)

    if len(argv) > 1:
        targets = [os.path.join(HERE, a) if not os.path.isabs(a) else a
                   for a in argv[1:]]
    else:
        targets = sorted(glob.glob(os.path.join(HERE, "*.md")))

    out_dir = os.path.join(HERE, "pdf")
    os.makedirs(out_dir, exist_ok=True)

    made = []
    for md_path in targets:
        if not os.path.isfile(md_path):
            print("MISS %s (not a file)" % md_path)
            continue
        with open(md_path, encoding="utf-8") as fh:
            text = fh.read()
        meta, _ = split_front_matter(text)
        if not meta.get("updated"):
            print("SKIP %s (no 'updated' front-matter field)"
                  % os.path.basename(md_path))
            continue
        try:
            pdf_path = render_md_to_pdf(md_path, out_dir, meta)
            made.append(pdf_path)
        except Exception as exc:  # noqa: BLE001 — report, don't crash the batch
            print("FAIL %s: %s" % (os.path.basename(md_path), exc))

    print("\nDone. %d PDF(s) written to %s" % (len(made), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
