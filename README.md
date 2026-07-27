# CV — Andrey Shigantsov

A bilingual résumé with automated PDF generation.

## Contents

| File | Purpose |
|------|---------|
| [`Andrey_Shigantsov_CV_English.md`](./Andrey_Shigantsov_CV_English.md) | English CV |
| [`Andrey_Shigantsov_CV_Russian.md`](./Andrey_Shigantsov_CV_Russian.md) | Russian CV |
| [`pdf/`](./pdf/) | Generated PDFs (build artifacts — safe to delete and regenerate) |
| `md-to-pdf.py` | Markdown → PDF build script (Python-Markdown + WeasyPrint) |
| `cv-style.css` | Print stylesheet for the PDFs (typography, NOTE callout, page breaks) |
| `AGENTS.md` | Rules for agents/editors: structure, version sync, mandatory script call |
| `Recomendations/` | Scanned recommendation letters, embedded into the CVs via markdown images |
| `tmp/` | Working materials (source PDF exports, samples) — git-ignored |

## Building the PDF

```bash
python3 md-to-pdf.py            # build PDFs from every eligible *.md
python3 md-to-pdf.py file.md    # build a specific file
```

Output goes to `pdf/` with the timestamp from the YAML front-matter leading the
file name: `<YYYYMMDDTHHMMSS>_<name>.pdf`. Previous versions are kept as history.

### Dependencies

- Python 3.8+
- `markdown`, `weasyprint`, `pyyaml` — on Arch: `sudo pacman -S python-markdown python-weasyprint python-yaml`
  (WeasyPrint pulls in the system libs pango/cairo/gdk-pixbuf/libffi).
- No Node.js, no headless browser.

## How to make changes

The CV exists in two language versions that must stay in sync. **All rules and
procedures are described in [`AGENTS.md`](./AGENTS.md)** — read it before
editing. Key points:

1. Any change is applied to **both** files (`*_English.md` and `*_Russian.md`).
2. Bump the `updated` field (ISO 8601) in the YAML front-matter of the file(s) you change.
3. After editing the markdown, always run `python3 md-to-pdf.py`.
