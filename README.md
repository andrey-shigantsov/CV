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
| `.vscode/` | VS Code workspace: `tasks.json` (`CV: Build PDFs` task), `settings.json` |
| `.github/workflows/` | CI: `cv-review.yml` — AI review of PR diffs against `AGENTS.md` |
| `AGENTS.md` | Rules for agents/editors: structure, version sync, mandatory script call |
| `Recomendations/` | Scanned recommendation letters, embedded into the CVs via markdown images |
| `tmp/` | Working materials (source PDF exports, samples) — git-ignored |

## Building the PDF

```bash
python3 md-to-pdf.py            # build PDFs from every eligible *.md
python3 md-to-pdf.py file.md    # build a specific file
```

Output goes to `pdf/<basename>.pdf` (e.g. `Andrey_Shigantsov_CV_English.pdf`) — a
single, fixed-name file per CV, overwritten on every run. No version history is
kept in `pdf/`; the current build date appears in the NOTE callout at the top of
the PDF (injected from the `updated` front-matter field).

From VS Code, run the **`CV: Build PDFs`** task (the default build task,
`Ctrl+Shift+B`) to rebuild all PDFs.

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
4. Keep `README.md` and `AGENTS.md` in sync — update them in the same change if
   it affects what they document (see AGENTS.md → *Documentation*).

Pull requests are auto-reviewed by CI (`.github/workflows/cv-review.yml`): a
GitHub Models LLM checks the diff against `AGENTS.md` and posts the findings as a
PR comment — a BLOCKER fails the check.
