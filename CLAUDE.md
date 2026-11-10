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
- File names contain ä/ö; links must match exactly. GitHub Pages is case-sensitive (`.JPEG` ≠ `.jpeg`), macOS is not.

## Current structure

```
index.html        Gallery. Inline <style> (~200 lines) and <script> (fade-in/out on navigation)
style.css         Shared stylesheet for story pages
audio.js          Story pages: music toggle, ripple pulses, back link
stories/          template.html + 4 story pages (tuulenpuuska, cordoba-ilmapallo,
                  eripintaiset-kasvot, frankenstein)
images/           Artwork .JPEG; "_leikattu" = cropped version
audio/            Soundscapes .mp3, plus drafts
```

Gallery markup: each section is `<div class="text-break"><em>Name</em></div>` followed by `<div class="gallery">` with `<div class="art-item SIZE">` tiles (img, optionally wrapped in `<a href="stories/x.html">`). Size rule in use: 3 works → `large`, 2 works → `huge`. The mobile CSS (≤ 768 px) has special rules for sections with exactly 2 or 3 works.

Story pages are ~95% identical boilerplate; only page title, heading, image, alt text, audio file and story text differ (paragraphs separated by `<br> <br>`).

## Goal

Make adding work easy enough that the site actually gets updated: write content in **Markdown in Typora**, generate the existing HTML with a small **Python build script** (standard library only). Chosen over Typora's HTML export (loses the design) and Jekyll (requires restructuring).

## Planned structure

```
content/
  gallery.md            ## Section → .text-break heading
                        ![Alt](../images/x.JPEG) → tile
                        [![Alt](../images/x.JPEG)](../stories/y.html) → tile linking to a story
                        ![Alt](../images/x.JPEG "wide") → size override
                        heading with no images → heading only ("Coming soon...")
  stories/<name>.md     front matter: title, image, audio, alt (optional)
                        body: plain paragraphs (blank line = new paragraph), *italic*, **bold**
                        image-only lines ignored (for Typora preview)
templates/story.html    story layout with {{title}} {{image}} {{alt}} {{audio}} {{body}}
build.py                regenerates index.html gallery block + stories/*.html
index.html              gallery block between <!-- GALLERY:START --> / <!-- GALLERY:END -->
stories/*.html          generated output, never edited by hand (URLs unchanged)
```

`python3 build.py --dry-run` shows a diff without writing. The build stops without writing anything if an image/audio/story file is missing or misspelled (case- and ä/ö-safe check).

A draft `build.py` exists (tested on a mock site). It still expects `gallery.md` in the root and `stories/*.md` next to the HTML; it needs updating for the `content/` folder and `../` paths.

## Step plan

1. **Tidy-up (first commit):** add `.gitignore` (`.DS_Store`); fix mismatched alt texts:
   - `lentokoulu.JPEG` has alt "Muuttolinnut"
   - `unimaailma.JPEG` has alt "Kaukana kotoa"
   - Frankenstein tile has alt "Frank"
   (Ask Lauri for the correct titles.)
2. **Content/design split:** add `content/`, `templates/story.html`, markers in `index.html`, updated `build.py`; migrate the current gallery and 4 stories to Markdown.
3. **Identical-output check:** build, `diff -w` against the current HTML (index.html has uneven indentation, so compare ignoring whitespace), click through locally (`python3 -m http.server`).
4. **Build warnings and unused files:** warn on sections with other than 2 or 3 works (mobile layout), list unused images/audio. About 11 images and 6 audio drafts are currently unused; decide whether to move them out of the repo.

Optional later: move index.html's inline CSS to its own file; make music optional in the story template; a Typora theme mimicking the site (Inter font); a GitHub Action that runs build.py on push.

## Open decisions

- Should story pages keep `lang="en"` or change to `fi`?
- Size rule for sections with 1 or 4+ works.
- Enable GitHub Pages for this repo (needs a public repo on a free account) once there is progress.
