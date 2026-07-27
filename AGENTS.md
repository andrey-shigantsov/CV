# AGENTS.md — CV (Andrey Shigantsov)

This file guides any agent (human or AI) editing the CV in this directory.
The CV is maintained in **two languages** that must stay structurally and
factually in sync.

## ⚠️ GLOBAL PRIORITY RULE (read first — overrides everything below)

> **В любой спорной или неоднозначной ситуации — спрашивай владельца, а не
> принимай решение сам.** Это приоритетное правило, оно стоит выше всех правил
> и конвенций в этом файле.

Specifically, STOP and ask the owner (via a clarifying question) before:
- **Any action that requires permissions you don't have** (e.g. installing
  system packages with `sudo`/`pacman`, modifying files outside the repo,
  entering credentials, granting access). Never silently skip such a step and
  never silently try a workaround — surface it.
- **Any irreversible or hard-to-reverse action** (deleting files you didn't
  create, overwriting, force-pushing, publishing, sending content externally,
  committing secrets).
- **Any fork in the road where multiple reasonable approaches exist** and the
  choice materially changes the outcome (architecture, library choice, public
  wording, data deletion vs. keeping, etc.).
- **Any contradiction** between the user's latest instruction and an earlier
  instruction or a rule in this file — resolve by asking, don't guess which
  wins.
- **Any step that just failed or is blocked** (missing tool, missing rights,
  failed install, network error) — report it and ask how to proceed instead of
  improvising a detour.

When in doubt: **ask, don't assume.** A quick question beats an hour of work in
the wrong direction. The rules below are defaults; this rule is the override.

## Files

| File | Language | Purpose |
|------|----------|---------|
| `Andrey_Shigantsov_CV_English.md` | English | Primary CV, used for international applications |
| `Andrey_Shigantsov_CV_Russian.md` | Russian | CV for Russian-speaking employers |
| `AGENTS.md` | — | This file: structure spec + sync checklist
| `md-to-pdf.py` | — | Pure-Python renderer: reads the `updated` timestamp, then converts each eligible `*.md` to a timestamped PDF in `pdf/` via Python-Markdown + WeasyPrint. Uses `cv-style.css`. |
| `cv-style.css` | — | Print stylesheet applied to all CV PDFs (typography, NOTE callout, page breaks). |
| `pdf/` | — | Generated PDFs; safe to delete and regenerate (not a source of truth) |
| `Recomendations/` | — | Source recommendation files (images/PDFs/…); **embedded into the RECOMENDATIONS section of the generated PDF** via markdown image syntax. Name format: `YYYYMMDD_<slug>[_<lang>].<ext>` (see *Section rules*) |

## Golden rule

> **The two CVs are translations of the same content.** Any factual or structural
> change made to one MUST be applied to the other in the same change.

## Sources of truth & conflict resolution

- **There is no single source of truth.** Only the two CV files
  (`*_English.md` and `*_Russian.md`) are tracked.
- **On any discrepancy between the two files, the most recently modified file
  wins.** Apply its content to the other file to bring them back into sync.
- After fixing, re-verify the sync checklist below.

## Required structure

Both files MUST follow the structure below. The exact section order and heading
text differ by language, but the sections themselves are identical and in this
order:

| # | English heading | Russian heading |
|---|-----------------|-----------------|
| 1 | `# Andrey Shigantsov` (H1 name) | `# Андрей Шиганцов` (H1 имя) |
| 2 | `**…role…**` (bold headline) | `**…роль…**` (жирным) |
| 3 | One-line contacts (see Contacts below) | Одна строка контактов |
| 4 | `## SUMMARY` | `## ОБО МНЕ` |
| 5 | `## EXPERIENCE` | `## ОПЫТ РАБОТЫ` |
| 6 | `## EDUCATION` | `## ОБРАЗОВАНИЕ` |
| 7 | `## SKILLS` | `## НАВЫКИ` |
| 8 | `## RECOMENDATIONS` | `## РЕКОМЕНДАЦИИ` |

### Section rules

- **YAML front-matter (MANDATORY):** the file MUST start with a front-matter
  block delimited by `---` lines. The block MUST contain exactly one field:
  ```yaml
  ---
  updated: 2026-07-27T13:45:57+06:00   # ISO 8601, with timezone
  ---
  ```
  - `updated` is the timestamp of the **last edit** to that file. Re-stamp it on
    every change, in the editor's local time, full ISO 8601 (date `T` time + UTC
    offset).
  - The timestamp MUST be identical in both language files when they are edited
    in the same change (i.e. kept in sync); if only one file changes, only its
    stamp is updated.
  - This timestamp feeds `md-to-pdf.py` (see *PDF generation* below).
- **NOTE callout (optional):** a single `> NOTE: …` blockquote immediately
  after the front-matter, before the H1 name. **It MUST be written in the
  file's own language** — the English NOTE is in English, the Russian NOTE in
  Russian (see *No language leakage — STRICT*). Both files SHOULD carry the
  same NOTE semantically (translated).
- **Header (name + headline + contacts):** H1 name, then a single bold role line,
  then a **single** contacts line separated by ` | `. No phone number.
- **SUMMARY:** 2–4 short paragraphs.
  - **The very first sentence MUST state the exact number of years of experience**
    (e.g., "Senior backend developer with **14+ years of experience**…").
    The number is the sum of non-overlapping employment durations from the
    EXPERIENCE section (gaps between jobs are excluded), rounded down to whole
    years with a `+` suffix. The number MUST be identical in both language files.
  - Must end with a `Desired role:` / `Желаемая роль:` line.
- **EXPERIENCE:** reverse-chronological (most recent first). Each entry:
  - `### Company name`
  - `**Role** — date range`
  - optional italic context line (`*Remote · …*`)
  - optional 1-line company description
  - bullet list of achievements/duties, each starting with `- `
  - within a company, multiple roles are allowed as separate bold role lines
- **EDUCATION:** one entry: degree, institution, years.
- **SKILLS:** grouped bullet list by category, each line `- **Category:** items`.
  Last line is always spoken languages:
  `- **Spoken languages:**` / `- **Разговорные языки:**`.
- **RECOMENDATIONS / РЕКОМЕНДАЦИИ:** the LAST section. Heading is
  **language-specific** (`## RECOMENDATIONS` in the EN file, `## РЕКОМЕНДАЦИИ`
  in the RU file) — like the other sections, it is translated. Lists
  recommendation files from the `Recomendations/` directory as **standard
  markdown images** (`![alt](./Recomendations/<file>)`, one per line), which
  `md-to-pdf.py` (Python-Markdown + WeasyPrint) **embeds directly into the
  generated PDF** (each file rendered on its own page of the section). The
  detector matches the heading case-insensitively, so either spelling is
  recognised.
  - **Files are embedded AS-IS — never transcribe, OCR, or paste their text.**
    The reader sees the file's content rendered inside the PDF, not a link.
  - **File-name format (MANDATORY):**
    ```
    YYYYMMDD_<slug>[_<lang>].<ext>
    ```
    - `YYYYMMDD` — the date of the recommendation (issue date), used for sorting.
    - `<slug>` — short descriptor, lowercase, words joined by `-`
      (e.g. `recomendation-v-latish`).
    - `<lang>` — **required language suffix**, one of `eng` / `rus`. A file
      appears ONLY in the CV of its matching language (a `…_rus.jpg` is listed
      in the Russian CV, `…_eng.pdf` in the English CV).
    - `<ext>` — any format: `.jpg`, `.png`, `.pdf`, `.docx`, … (WeasyPrint
      embeds raster images natively; vector/PDF assets are rasterised by its
      GDK-PixBuf backend).
    - Example: `20260717_a-shigantsov_recomendation-v-latish_eng.jpg`.
  - **Ordering:** reverse-chronological by the `YYYYMMDD` prefix (newest first).
    Ties broken alphabetically by the rest of the name.
  - **Image syntax:** `![<alt>](./Recomendations/<filename>)` — use the
    standard markdown image form so `md-to-pdf.py` embeds the file. `<alt>`
    should echo the slug without the date/lang (e.g.
    `![recomendation-v-latish_eng](./Recomendations/…_eng.jpg)`). Always use
    `./` (relative to the markdown file) so the path resolves at render time.
  - Both language files MUST list the same set of recommendations *for their
    language* (same dates, same sources) — i.e. an `_eng` file and a `_rus`
    counterpart describe the same recommendation and stay paired.

### Contacts (canonical, both files must match)

| Field | Value |
|-------|-------|
| Email | `a.shigantsov@gmail.com` |
| Telegram | `@rasaro89` → `https://t.me/rasaro89` |
| GitHub | `https://github.com/andrey-shigantsov` |
| GitLab | `https://gitlab.com/andrey-shigantsov` |
| Portfolio | `https://docs.google.com/presentation/d/1cu0rpvXFcqgHSNspt4M0GizctlspQlxM6nvBHP9CE2k/edit?usp=sharing` |

- **No phone number** anywhere in the CV (removed by request; replaced by Telegram).
- Order in the contacts line: Email · Telegram · GitHub · GitLab · Portfolio.

## Sync checklist (run after every edit)

Before considering an edit done, verify all of the following:

1. **Both files edited.** Any fact/structure change applied to both
   `*_English.md` and `*_Russian.md`. If you only touched one, stop and fix the other.
2. **Section count and order match.** Both files have exactly the 8 sections
   above in the same order. Same H2 headings per the table.
3. **Experience entries match 1:1.** Same companies, same order, same date ranges,
   same number of roles per company, same number of bullets per role.
   Count them in both files and compare.
4. **Skills categories match.** Same set of category bullets, same order. Same
   items inside each category.
5. **Contacts match the canonical table above.** No phone number present.
6. **No discrepancies between the two files.** Company names, dates, degree,
   institution, tech stack, links — all must be consistent across
   `*_English.md` and `*_Russian.md`. If a discrepancy is found, resolve it by
   trusting the most recently modified file (see *Conflict resolution* above),
   then propagate to the other file.
7. **No language leakage — STRICT.** Each file is written ENTIRELY in its
   language. The English file contains **no Russian words** (sentences,
   phrases, headings, NOTE/quote blocks, anything authored for the CV) — and
   vice versa for the Russian file. This includes every block the agent might
   add (e.g. a NOTE callout): write it in the file's own language. Do not copy
   a Russian NOTE verbatim into the English file or the reverse.
   - **Sole exception — official proper nouns** (company legal names, place
     names, institution/award names): render in the file's language, with the
     original-language name in parentheses, e.g.
     `STREAM TECH LLC (ООО «СТРИМ ТЕХ»)`, `Siberian State Automobile and
     Highway Academy (СибАДИ)`. The parenthetical original is allowed ONLY for
     such proper nouns, never for prose.
   - **Tech terms are language-neutral** (Rust, tokio, gRPC, …) — kept verbatim
     in both files, never transliterated.
8. **Links render as markdown.** Every URL is either in `[text](url)` form or is a
   bare URL; verify no broken `[` / `]` / `()` pairing.
9. **RECOMENDATIONS section.** Heading is `## RECOMENDATIONS` (EN) /
   `## РЕКОМЕНДАЦИИ` (RU) — translated. Every file in `Recomendations/` matching
   the file-name format with the right `_lang` suffix is referenced as a
   markdown image `![alt](./Recomendations/…)` in the matching CV; none is
   transcribed as text; ordering is reverse-chronological. The two CVs expose
   the same recommendations (paired `_eng` / `_rus`). `md-to-pdf.py` embeds each
   listed file in-page into the PDF — verify the generated PDF actually contains
   the rendered recommendation pages (large embedded image), not the alt text.

## Editing conventions

- **Language of edits:** match each file's language. Do not auto-translate
  blindly — adapt phrasing naturally (e.g. "Lead" → "Руководитель", not "Лид").
- **Bullet style:** `- ` (hyphen + space). One achievement per bullet, action verb first.
- **Dates:** English `Mon YYYY – Mon YYYY` / `– Present`; Russian `мон. ГГГГ – мон. ГГГГ` / `– настоящее время`.
- **Tech stack:** keep English/technical names as-is in both files (Rust, tokio,
  PostgreSQL, Kafka, etc.) — do not transliterate or translate tool names.
- **Open-source links:** render as `[repo-name](url)`; group under a **bold**
  `Open source` / `Открытый код` sub-label inside the relevant company's bullets.
- **Headline role:** keep in sync between the H2-sub header and the SUMMARY's
  `Desired role` line.

## PDF generation (MANDATORY after every markdown change)

> **Iron rule:** after ANY change to a `*.md` CV file, run `md-to-pdf.py`
> **before** considering the task done. The two CVs and their PDFs must never be
> out of sync.

`md-to-pdf.py` converts every eligible `*.md` in this directory to a PDF in
`./pdf/`. "Eligible" = has a YAML front-matter `updated` field. Files without it
(e.g. `AGENTS.md`) are skipped automatically.

**Run:**
```bash
python3 md-to-pdf.py                       # convert all eligible *.md
python3 md-to-pdf.py Andrey_Shigantsov_CV_English.md   # convert one file
```

**Output naming:** `<updated-normalised>_<basename>.pdf` — the timestamp leads
the file name, e.g.
`20260727T134557_Andrey_Shigantsov_CV_English.pdf`. The `updated` ISO 8601
value is normalised to `YYYYMMDDTHHMMSS` (timezone dropped for file-name
portability). Leading timestamp keeps PDFs sorted newest-first by default in
directory listings.

Rules:
- Each run produces a fresh timestamped PDF (previous ones are kept as history).
- `pdf/` is a build artifact, not a source of truth — never hand-edit PDFs
  there; regenerate from the markdown instead.
- If `md-to-pdf.py` reports `SKIP` for a CV, the CV is missing its `updated`
  front-matter field — fix the markdown, don't skip the PDF step.

**Pipeline & dependencies:**
- `md-to-pdf.py` is a **pure-Python renderer** — it has **no Node.js and no
  headless browser** dependency. It uses **Python-Markdown** for markdown →
  HTML and **WeasyPrint** for HTML+CSS → PDF. All real rendering (headings,
  lists, links, blockquotes, `![](image)` embedding, code blocks) is done by
  these standard Python libraries — do not reinvent parsing or rendering in
  the script.
- Styling lives in `cv-style.css` (typography, the NOTE callout, page breaks
  for RECOMENDATIONS). WeasyPrint honours standard print CSS, including
  `@page { size; margin }`. Edit styles there, not in the script.
- **Requirements:** Python 3 + `markdown`, `weasyprint`, `pyyaml`. On Arch:
  `sudo pacman -S python-markdown python-weasyprint python-yaml`. WeasyPrint
  needs the system libs pango/cairo/gdk-pixbuf/libffi, which `pacman` pulls in
  automatically. If `md-to-pdf.py` reports `FAIL`, check that WeasyPrint is
  installed and its system libs are present (`python3 -c "import weasyprint"`
  prints a clear error otherwise).

## Common pitfalls to avoid

- Editing only one language file → breaks sync (rule 1).
- Inventing facts not present in either file (no fabrication; ask the owner instead).
- Renaming companies or translating them inconsistently between files.
- Adding a phone number back (it was intentionally removed).
- Reordering sections away from the reference sample's order.
- Changing one file's bullet count without mirroring in the other.
