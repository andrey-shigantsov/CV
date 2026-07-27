#!/usr/bin/env python3
"""
md_to_pdf.py — Convert CV markdown files to timestamped PDFs.

Reads every ``*.md`` file in this script's directory that carries a YAML
front-matter block with an ``updated`` field (ISO 8601), and renders each to
PDF in ``./pdf/`` with the timestamp appended to the file name.

Files without a front-matter ``updated`` field (e.g. ``AGENTS.md``) are skipped.

Dependencies: reportlab, pyyaml (PyYAML). Fonts are resolved via ``fc-match``.

Usage:
    python3 md_to_pdf.py                # convert all eligible *.md
    python3 md_to_pdf.py file.md [...]  # convert specific file(s)
"""

import os
import re
import sys
import glob
import subprocess

import yaml
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --------------------------------------------------------------------------
# Fonts (DejaVu — full Cyrillic + the special chars used in the CVs)
# --------------------------------------------------------------------------

def _fc_match(family: str) -> str:
    """Return the TTF path for a font family/style via fontconfig."""
    try:
        r = subprocess.run(
            ["fc-match", "-f", "%{file}", family],
            capture_output=True, text=True, check=False,
        )
        path = r.stdout.strip()
        if path and os.path.exists(path):
            return path
    except (FileNotFoundError, OSError):
        pass
    return ""


def register_fonts() -> None:
    sans = _fc_match("DejaVu Sans")
    sans_bold = _fc_match("DejaVu Sans:style=Bold")
    sans_italic = _fc_match("DejaVu Sans:style=Oblique")
    sans_bolditalic = _fc_match("DejaVu Sans:style=Bold Oblique")
    mono = _fc_match("DejaVu Sans Mono")

    if not sans:
        sys.exit("ERROR: DejaVu Sans font not found via fc-match. "
                 "Install fonts-dejavu.")

    pdfmetrics.registerFont(TTFont("CVSans", sans))
    if sans_bold:
        pdfmetrics.registerFont(TTFont("CVSans-Bold", sans_bold))
    if sans_italic:
        pdfmetrics.registerFont(TTFont("CVSans-Italic", sans_italic))
    if sans_bolditalic:
        pdfmetrics.registerFont(TTFont("CVSans-BoldItalic", sans_bolditalic))
    if mono:
        pdfmetrics.registerFont(TTFont("CVMono", mono))

    # Map <b>/<i> markup to the registered variants.
    pdfmetrics.registerFontFamily(
        "CVSans",
        normal="CVSans",
        bold=sans_bold and "CVSans-Bold" or "CVSans",
        italic=sans_italic and "CVSans-Italic" or "CVSans",
        boldItalic=sans_bolditalic and "CVSans-BoldItalic" or "CVSans",
    )


# --------------------------------------------------------------------------
# Inline markdown → ReportLab markup
# --------------------------------------------------------------------------

def _esc(s: str) -> str:
    """Escape XML-special chars for safe use inside ReportLab markup."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def _esc_attr(s: str) -> str:
    """Escape for use inside an attribute value (URLs)."""
    return _esc(s).replace('"', "&quot;")


def md_inline(text: str) -> str:
    """
    Convert a substring of inline markdown to ReportLab paragraph markup.

    Supports: `` `code` ``, `` [label](url) ``, `` **bold** ``, `` *italic* ``.
    Nesting is handled recursively (e.g. bold inside a link label).
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        # inline code  `...`
        if text[i] == "`":
            j = text.find("`", i + 1)
            if j != -1:
                mono_face = "CVMono" if "CVMono" in pdfmetrics.getRegisteredFontNames() else "CVSans"
                out.append('<font face="%s">%s</font>'
                           % (mono_face, _esc(text[i + 1:j])))
                i = j + 1
                continue
        # link  [label](url)
        if text[i] == "[":
            j = text.find("]", i + 1)
            if j != -1 and j + 1 < n and text[j + 1] == "(":
                k = text.find(")", j + 2)
                if k != -1:
                    label = text[i + 1:j]
                    url = text[j + 2:k]
                    out.append('<link href="%s" color="#0b5fa5">%s</link>'
                               % (_esc_attr(url), md_inline(label)))
                    i = k + 1
                    continue
        # bold  **...**
        if text[i:i + 2] == "**":
            j = text.find("**", i + 2)
            if j != -1:
                out.append("<b>%s</b>" % md_inline(text[i + 2:j]))
                i = j + 2
                continue
        # italic  *...*
        if text[i] == "*":
            j = text.find("*", i + 1)
            if j != -1:
                out.append("<i>%s</i>" % md_inline(text[i + 1:j]))
                i = j + 1
                continue
        # plain character
        c = text[i]
        out.append(_esc(c) if c in "&<>" else c)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# Front-matter
# --------------------------------------------------------------------------

def split_front_matter(text: str):
    """
    Return (meta_dict, body_text). meta is {} if no front-matter.
    A front-matter block is a leading ``---\\n ... \\n---``.
    """
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

    Accepts any ISO 8601 timestamp (e.g. ``2026-07-27T13:45:57+06:00``) and
    normalises it to a compact, file-name-safe form: ``YYYYMMDDTHHMMSS``.
    The date+time (to the second) is what matters for versioning; the timezone
    offset is dropped because it is not portable across file systems and
    produces ugly names. The field is preserved unchanged in the markdown.
    """
    updated = meta.get("updated")
    if not updated:
        return ""
    s = str(updated).strip()
    # Normalise: keep digits only in the date/time portion.
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
# Styles
# --------------------------------------------------------------------------

INK = HexColor("#1a1a1a")
MUTED = HexColor("#555555")
ACCENT = HexColor("#0b3d62")
RULE = HexColor("#cfcfcf")

BODY_FS = 10
NAME_FS = 22


def make_styles():
    base = dict(fontName="CVSans")
    return {
        "name": ParagraphStyle("name", **base, fontSize=NAME_FS,
                               textColor=INK, leading=NAME_FS + 4, spaceAfter=2),
        "headline": ParagraphStyle("headline", **base, fontSize=12.5,
                                   textColor=ACCENT, leading=16, spaceAfter=6),
        "contacts": ParagraphStyle("contacts", **base, fontSize=9,
                                   textColor=MUTED, leading=13, spaceAfter=2),
        "h2": ParagraphStyle("h2", **base, fontSize=13, textColor=ACCENT,
                             leading=16, spaceBefore=14, spaceAfter=4),
        "h3": ParagraphStyle("h3", **base, fontSize=11.5, textColor=INK,
                             leading=15, spaceBefore=10, spaceAfter=2),
        "body": ParagraphStyle("body", **base, fontSize=BODY_FS, textColor=INK,
                               leading=14, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", **base, fontSize=BODY_FS, textColor=INK,
                                 leading=13.5, leftIndent=16, bulletIndent=3,
                                 spaceAfter=3),
        "subbullet": ParagraphStyle("subbullet", **base, fontSize=BODY_FS,
                                    textColor=INK, leading=13.5, leftIndent=34,
                                    bulletIndent=20, spaceAfter=2),
    }


# --------------------------------------------------------------------------
# Block parser → flowables
# --------------------------------------------------------------------------

def build_flowables(body: str, styles):
    lines = body.splitlines()
    flows = []
    i, n = 0, len(lines)

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        # horizontal rule
        if stripped == "---":
            flows.append(Spacer(1, 4))
            flows.append(HRFlowable(width="100%", thickness=0.5,
                                    color=RULE, spaceBefore=2, spaceAfter=6))
            i += 1
            continue

        # headings
        if stripped.startswith("### "):
            flows.append(Paragraph(md_inline(stripped[4:]), styles["h3"]))
            i += 1
            continue
        if stripped.startswith("## "):
            flows.append(Paragraph(md_inline(stripped[3:]), styles["h2"]))
            flows.append(HRFlowable(width="100%", thickness=0.4,
                                    color=RULE, spaceBefore=1, spaceAfter=4))
            i += 1
            continue
        if stripped.startswith("# "):
            flows.append(Paragraph(md_inline(stripped[2:]), styles["name"]))
            i += 1
            continue

        # bullet block (top + nested, possibly multi-line)
        if stripped.startswith("- ") or raw.lstrip().startswith("- "):
            block_flows = []
            while i < n:
                bline = lines[i]
                bstrip = bline.strip()
                if not bstrip:
                    # blank line ends the bullet block
                    break
                indent = len(bline) - len(bline.lstrip())
                if bstrip.startswith("- "):
                    text = bstrip[2:]
                    if indent >= 2:
                        st = styles["subbullet"]
                        marker = "◦"
                    else:
                        st = styles["bullet"]
                        marker = "•"
                    block_flows.append(
                        Paragraph(md_inline(text), st, bulletText=marker))
                    i += 1
                    continue
                # non-bullet line ends the bullet block
                break
            # keep bullets visually grouped
            flows.extend(block_flows)
            continue

        # paragraph
        flows.append(Paragraph(md_inline(stripped), styles["body"]))
        i += 1

    return flows


# --------------------------------------------------------------------------
# Render one file
# --------------------------------------------------------------------------

def render(md_path: str, out_dir: str) -> str:
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()

    meta, body = split_front_matter(text)
    suffix = timestamp_suffix(meta)
    if not suffix:
        print("SKIP %s (no 'updated' front-matter field)" % os.path.basename(md_path))
        return ""

    base = os.path.splitext(os.path.basename(md_path))[0]
    pdf_name = "%s_%s.pdf" % (base, suffix)
    pdf_path = os.path.join(out_dir, pdf_name)

    styles = make_styles()
    flows = build_flowables(body, styles)

    # Author / title metadata from the document.
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else base

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title=title, author=title,
        subject="Curriculum Vitae",
        creator="md_to_pdf.py",
    )
    doc.build(flows)
    print("OK   %s -> %s" % (os.path.basename(md_path), pdf_name))
    return pdf_path


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    register_fonts()

    if len(argv) > 1:
        targets = [os.path.join(here, a) if not os.path.isabs(a) else a
                   for a in argv[1:]]
    else:
        targets = sorted(glob.glob(os.path.join(here, "*.md")))

    out_dir = os.path.join(here, "pdf")
    os.makedirs(out_dir, exist_ok=True)

    made = []
    for md_path in targets:
        if not os.path.isfile(md_path):
            print("MISS %s (not a file)" % md_path)
            continue
        pdf_path = render(md_path, out_dir)
        if pdf_path:
            made.append(pdf_path)

    print("\nDone. %d PDF(s) written to %s" % (len(made), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
