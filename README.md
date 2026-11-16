# Matkalla

**Matkalla** is a small online gallery of my drawings. Some drawings have a story page with a short text and a soundscape. This is the second version of the website.

Live site: https://laurilaurilauri.github.io/uudella-matkalla/

How it works:

- **Content is written in Markdown** in Typora: the gallery and the story texts.
- **Content and design are kept apart.** The Markdown files say what is on the site; the look comes from the CSS files and a page template.
- **Two small Python scripts do the rest.** `shrink.py` makes web-size images, `build.py` turns the Markdown into the HTML pages. No HTML is edited by hand.

---

## Adding drawings and a story

The example adds a new section *Talvi* with three drawings, one of which has the story *Jäätynyt järvi*.

### 1. Add the image files

Put the full-size photos into `originals/`, and the soundscape (if the story has one) into `audio/`:

```
originals/lumiukko.jpg
originals/jaatynyt-jarvi.jpg
originals/pakkasaamu.jpg
audio/talvi.mp3
```

**Names:** lowercase, hyphens between words, no ä/ö, no spaces. *Jäätynyt järvi* → `jaatynyt-jarvi.jpg`. Capital letters matter online: `.jpg` and `.JPG` are different files.

Then make the web-size copies into `images/`:

```bash
python3 shrink.py
```

Originals may also be `.jpeg`, `.png` or `.heic` (iPhone); the copy in `images/` always ends in `.jpg`. The Markdown files always link to `images/`, never to `originals/`.

### 2. Write the story (skip if there is no story)

Copy an existing file in `content/stories/` to a new name. The file name becomes the page address: `jaatynyt-jarvi.md` → `stories/jaatynyt-jarvi.html`. Same naming rule as above.

```markdown
---
title: Jäätynyt järvi
audio: ../../audio/talvi.mp3
---

![Jäätynyt järvi](../../images/jaatynyt-jarvi.jpg)

First paragraph.

Second paragraph, with *italic* and **bold**.
```

- `title` is the page heading and the browser tab name.
- `audio` is optional. Leave the line out for a story without a soundscape: the page then has no music button and no "Äänimaailma by me" line.
- The image line right below the top block is the story's drawing.
- A blank line starts a new paragraph. Only `*italic*` and `**bold**` are supported for now (headings, lists and links would need their own styling first).

### 3. Add the section to the gallery

In `content/gallery.md`, a `##` heading starts a section and each image line is one drawing. The order in the file is the order on the page.

```markdown
## Talvi

![Lumiukko](../images/lumiukko.jpg)
[![Jäätynyt järvi](../images/jaatynyt-jarvi.jpg)](stories/jaatynyt-jarvi.md)
![Pakkasaamu](../images/pakkasaamu.jpg)
```

- The name in `[...]` is the drawing's name (alt text).
- The middle line is a drawing that opens a story: the image wrapped in a link to the story's `.md` file. In Typora: select the image, Cmd+K, choose the file.
- A section should have **2 or 3 drawings**: the mobile layout is made for those. Three are shown large, two are shown huge.
- A `##` heading with no images is shown on its own (like "Coming soon...").

### 4. Build and check

```bash
python3 build.py --dry-run     # show what would change, write nothing
python3 build.py               # write the pages
python3 -m http.server 8000    # preview at http://localhost:8000
```

If a file name is misspelled, the build stops, names the file and line, and writes nothing. In the preview, check the new section, the story link, the music and the back link, also in a narrow window (mobile).

### 5. Commit and push

Commit everything together: images, audio, Markdown files and the generated HTML (`git add -A`). Git ignores `originals/`, so the full-size photos stay on the computer (backed up in iCloud). The live site updates a minute or two after the push.

---

## The scripts

### `build.py`: Markdown → HTML

| Edited by me | The build writes |
|---|---|
| `content/gallery.md` | `index.html`: only the gallery part between `<!-- GALLERY:START -->` and `<!-- GALLERY:END -->`, plus the page title |
| `content/stories/<name>.md` | `stories/<name>.html`, using the layout in `templates/story.html` |

The generated parts are never edited by hand: the next build would overwrite them.

**Safety checks.** The build stops and writes nothing if an image, audio file or story doesn't exist exactly as written, a required setting is missing or misspelled, or a line doesn't follow the format. It lists every problem, for example:

```
  - content/gallery.md, line 8: image not found: '../images/surullinen-kuu.JPG' (the file is called 'surullinen-kuu.jpg': check capital letters)
```

**Warnings** don't stop the build, they point out things worth checking (e.g. a section with other than 2 or 3 drawings).

### `shrink.py`: web-size images

Makes a copy in `images/` of every image in `originals/`:

- Longer side over 2400 px: shrunk to 2400 px and saved as JPEG quality 85.
- 2400 px or less: copied as it is (saving it again would only make it bigger).
- Images that are already up to date are skipped. Replacing an original with an edited version updates its copy on the next run. Originals are never changed.

It uses the Mac's built-in `sips` tool. On Windows, only this file would need changing (e.g. to use the Pillow library).

---

## Project structure

```
uudella-matkalla/
├── content/              # What is on the site (edited by me)
│   ├── gallery.md        #   front page: title, sections, drawings
│   └── stories/          #   one .md file per story
├── originals/            # Full-size photos (not in git)
├── images/               # Web-size copies made by shrink.py
├── audio/                # Soundscapes (.mp3) from BandLab and GarageBand
│
├── build.py              # Markdown → HTML
├── shrink.py             # originals/ → images/
├── templates/story.html  # Layout of a story page
│
├── index.html            # Front page (gallery part generated by build.py)
├── gallery.css           # Front page styles
├── gallery.js            # Front page: fade between pages
├── stories/              # Story pages (generated by build.py)
├── style.css             # Story page styles
├── audio.js              # Story pages: music button, animation, back link
│
├── README.md             # This file
├── STATUS.md             # Work in progress, plans and decisions
└── CLAUDE.md             # Project notes for Claude Code
```

---

## How the pages work

**Front page** (`index.html`, `gallery.css`, `gallery.js`)

- Each section is a heading followed by a grid of drawings. On mobile (≤ 768 px) the grid becomes rows of equal tiles.
- Drawings lift slightly on hover.
- Pages fade in on load and fade out when moving to another page of the site.
- The font is Inter, from Google Fonts.

**Story pages** (`templates/story.html`, `style.css`, `audio.js`)

```
← TAKAISIN TAIDEGALLERIAAN        (back link)
┌───────────────┐   Title
│               │   [ Uppoudu äänimaailmaan ]   (music button, only with audio)
│    drawing    │   Story text…
│               │
└───────────────┘   Äänimaailma by me            (only with audio)
```

- Drawing and text side by side on desktop, stacked on mobile.
- The music button plays the soundscape on a loop; its label switches to "Keskeytä kokemus" while playing.
- While music plays, small circles spread over the drawing like raindrops. The plan is to develop this animation further later.
- The back link returns to the gallery where the visitor left it.

**Files:** names ending in `-leikattu` ("cropped") are the cropped versions used on the site. `originals/` and `images/` also hold drawings not on the site yet, and `audio/` keeps earlier drafts and mixes (`-kesken` = unfinished, `-faded`, `-mastered`, …).

---

## Typora theme

A Typora theme called *Matkalla* shows images at half size while writing. It is saved as `matkalla.css` in Typora's themes folder (Typora → Preferences → Appearance → Open Theme Folder), outside the project:

```css
@import url("github.css");
#write img { zoom: 50%; }
```

---

[GitHub repository](https://github.com/laurilaurilauri/uudella-matkalla) · © Lauri Prudant 2026
