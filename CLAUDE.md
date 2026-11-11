# Uudella matkalla — project context

## What this is

Lauri's hand-built online gallery of drawings, mostly from travels in South America and after returning to Finland. Some works have a **story page**: a short Finnish text plus an original soundscape (BandLab / GarageBand) the visitor can play.

- **This repo:** `laurilaurilauri/uudella-matkalla`, local folder `~/LocalProjects/uudella-matkalla`. A copy (with full history) of the original site, created for improvements.
- **Original site (do not touch):** repo `laurilaurilauri/matkalla`, live at https://laurilaurilauri.github.io/matkalla/. It stays as it is until the new version is ready.
- **Tech:** plain HTML, CSS, JavaScript. No frameworks, build tools or dependencies. Hosted on GitHub Pages.
- **Language:** page content and story texts are in Finnish.

## Ground rules

- The site's look and behaviour must stay identical unless Lauri explicitly asks for a design change.
- Keep it simple enough that Lauri (some coding knowledge, not a web developer) can always understand how it works. Explain changes in plain terms.
- Show proposed changes before applying them. One step at a time, one commit per step.
- Lauri always makes the commits himself. Never run `git commit` or `git push`; prepare the changes and leave them for Lauri to review and commit.
- Current progress, the plan and decisions are in STATUS.md. Read it at the start of a session and keep it updated as work progresses.
- How to write STATUS.md: it is for Lauri to read first, so readability comes before completeness. Plain language, short sections, no clutter. Use inline `code` only when really necessary (e.g. a command to type); write file and folder names as plain text otherwise. Remove completed work, except the most recently completed step, which stays as ~~struck-through~~ text so it's clear where things left off. Record decisions briefly with the reason.
- File names contain ä/ö; links must match exactly. GitHub Pages is case-sensitive (`.JPEG` ≠ `.jpeg`), macOS is not.

## Goal

Make adding work easy enough that the site actually gets updated: write content in **Markdown in Typora** (content/), generate the existing HTML with a small **Python build script** (build.py, standard library only). Chosen over Typora's HTML export (loses the design) and Jekyll (requires restructuring).

## Build

- `python3 build.py --dry-run` shows a diff without writing. The build stops without writing anything if an image/audio/story file is missing or misspelled (case- and ä/ö-safe check).
- stories/*.html and the gallery block in index.html (between the GALLERY:START / GALLERY:END markers) are generated output: edit content/ and templates/, never the generated HTML by hand. Story URLs must not change.
- Gallery size rule: 3 works → `large`, 2 → `huge`. The mobile CSS (≤ 768 px) only handles sections with exactly 2 or 3 works.

## Open decisions

- Should story pages keep `lang="en"` or change to `fi`?
- Enable GitHub Pages for this repo (needs a public repo on a free account) once there is progress.
