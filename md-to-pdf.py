#!/usr/bin/env python3
"""
md-to-pdf.py — Convert CV markdown files to timestamped PDFs.

Pure-Python pipeline (no Node.js, no headless browser):
  markdown  — parses the markdown source to HTML (Python-Markdown).
  weasyprint — renders that HTML + cv-style.css to a PDF.

Reads every ``*.md`` file in this script's directory that carries a YAML
front-matter block with an ``updated`` field (ISO 8601), and renders each to
PDF in ``./pdf/`` with the timestamp appended to the file name.

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


def timestamp_suffix(meta: dict) -> str:
    """
    File-name-safe suffix from the ``updated`` field, or '' if absent.
    Any ISO 8601 value → compact ``YYYYMMDDTHHMMSS`` (timezone dropped).
    """
    updated = meta.get("updated")
    if not updated:
        return ""
    s = str(updated).strip()
    m = re.match(
        r"(\d{4})\D?(\d{2})\D?(\d{2})[T ]?(\d{2})?\D?(\d{2})?\D?(\d{2})?", s)
    if not m:
        return ""
    y, mo, d = m.group(1), m.group(2), m.group(3)
    hh = m.group(4) or "00"
    mm = m.group(5) or "00"
    ss = m.group(6) or "00"
    return "%s%s%sT%s%s%s" % (y, mo, d, hh, mm, ss)


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_md_to_pdf(md_path: str, out_dir: str, suffix: str) -> str:
    """
    Render one markdown file to PDF via Python-Markdown + WeasyPrint, writing
    to <out_dir>/<basename>_<suffix>.pdf. Returns the final PDF path.
    """
    import markdown  # imported lazily so --help works without the dep
    from weasyprint import HTML

    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    _, body = split_front_matter(text)

    base = os.path.splitext(os.path.basename(md_path))[0]
    final_name = "%s_%s.pdf" % (suffix, base)
    final_path = os.path.join(out_dir, final_name)

    # Markdown → HTML. The document title (H1) doubles as the PDF <title>.
    html_body = markdown.markdown(body, extensions=MD_EXTENSIONS)
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
        suffix = timestamp_suffix(meta)
        if not suffix:
            print("SKIP %s (no 'updated' front-matter field)"
                  % os.path.basename(md_path))
            continue
        try:
            pdf_path = render_md_to_pdf(md_path, out_dir, suffix)
            made.append(pdf_path)
        except Exception as exc:  # noqa: BLE001 — report, don't crash the batch
            print("FAIL %s: %s" % (os.path.basename(md_path), exc))

    print("\nDone. %d PDF(s) written to %s" % (len(made), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
