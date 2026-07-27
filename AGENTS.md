# AGENTS.md — CV (Andrey Shigantsov)

This file guides any agent (human or AI) editing the CV in this directory.
The CV is maintained in **two languages** that must stay structurally and
factually in sync.

## Files

| File | Language | Purpose |
|------|----------|---------|
| `Andrey_Shigantsov_CV_English.md` | English | Primary CV, used for international applications |
| `Andrey_Shigantsov_CV_Russian.md` | Russian | CV for Russian-speaking employers |
| `AGENTS.md` | — | This file: structure spec + sync checklist
| `md_to_pdf.py` | — | Renders every eligible `*.md` to a timestamped PDF in `pdf/` |
| `pdf/` | — | Generated PDFs; safe to delete and regenerate (not a source of truth) |

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
  - This timestamp feeds `md_to_pdf.py` (see *PDF generation* below).
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
2. **Section count and order match.** Both files have exactly the 7 sections
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
7. **No language leakage.** English file contains no Russian words (except proper
   nouns / company names given in Russian original, rendered in English).
   Russian file contains no stray English words where a Russian term is expected.
8. **Links render as markdown.** Every URL is either in `[text](url)` form or is a
   bare URL; verify no broken `[` / `]` / `()` pairing.

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

> **Iron rule:** after ANY change to a `*.md` CV file, run `md_to_pdf.py`
> **before** considering the task done. The two CVs and their PDFs must never be
> out of sync.

`md_to_pdf.py` converts every eligible `*.md` in this directory to a PDF in
`./pdf/`. "Eligible" = has a YAML front-matter `updated` field. Files without it
(e.g. `AGENTS.md`) are skipped automatically.

**Run:**
```bash
python3 md_to_pdf.py                       # convert all eligible *.md
python3 md_to_pdf.py Andrey_Shigantsov_CV_English.md   # convert one file
```

**Output naming:** `<basename>_<updated-normalised>.pdf`, where the `updated`
ISO 8601 value is normalised to `YYYYMMDDTHHMMSS` (timezone dropped for
file-name portability), e.g.
`Andrey_Shigantsov_CV_English_20260727T134557.pdf`.

Rules:
- Each run produces a fresh timestamped PDF (previous ones are kept as history).
- `pdf/` is a build artifact, not a source of truth — never hand-edit PDFs
  there; regenerate from the markdown instead.
- If `md_to_pdf.py` reports `SKIP` for a CV, the CV is missing its `updated`
  front-matter field — fix the markdown, don't skip the PDF step.

## Common pitfalls to avoid

- Editing only one language file → breaks sync (rule 1).
- Inventing facts not present in either file (no fabrication; ask the owner instead).
- Renaming companies or translating them inconsistently between files.
- Adding a phone number back (it was intentionally removed).
- Reordering sections away from the reference sample's order.
- Changing one file's bullet count without mirroring in the other.
