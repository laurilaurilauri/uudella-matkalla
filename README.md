# Matkalla — laurin-taidenurkkaus

*Kokeilu nettisivusta* — a personal art portfolio website by Lauri Prudant.

Link: https://laurilaurilauri.github.io/matkalla/

**Matkalla** ("On the way") is a small, hand-built online gallery of drawings. Most of the pieces were made while travelling in South America and after coming back to Finland. Some works have their own **story page**: a short text in Finnish about how the piece came to be, plus an original soundscape that the visitor can play while looking at the image.

The site is plain HTML, CSS and JavaScript. It has no frameworks, build tools or dependencies, so it runs as is in any modern browser.

---

## Project structure

```
laurin-taidenurkkaus/
├── index.html          # Main gallery page ("Matkalla"), with its own inline CSS and JS
├── style.css           # Shared stylesheet for all story pages
├── audio.js            # Shared script for story pages: music toggle, ripple animation, back link
├── stories/            # One HTML page per story
│   ├── template.html           # Starting point for new story pages
│   ├── tuulenpuuska.html       # "Tuulenpuuska"
│   ├── cordoba-ilmapallo.html  # "Vaikea valinta"
│   ├── eripintaiset-kasvot.html# "Kasvoja kadulla ja seinillä"
│   └── frankenstein.html       # "Frankenstein"
├── images/             # Artwork photos (.JPEG); "_leikattu" = cropped version
├── audio/              # Soundscapes (.mp3) made in BandLab and GarageBand
├── .gitattributes      # Line-ending normalisation
└── README.md
```

---

## Main gallery — `index.html`

The front page is self-contained: its styles live in a `<style>` block and its behaviour in a `<script>` block at the end of the file. It doesn't use `style.css` or `audio.js`.

### Themed sections

Artworks are grouped into themed sections. Each section has a heading (`.text-break`) followed by its own `.gallery` grid:

| Section | Works |
|---|---|
| *Uusia tuulia* | Surullinen kuu · **Tuulenpuuska** ↗ · Lempeä horisontti |
| *Katse* | **Cordoban ilmapallo** ↗ · **Eripintaiset naamat** ↗ · **Frankenstein** ↗ |
| *Kohtaamisia ja kukkia* | Palapeli · Hahmo ja lintu · Kukat vievät |
| *Lento* | Lentokoulu · Unimaailma |
| *Ruokaketju* | Ruokaketju · Juurikaupunki |
| *Yksinäinen/yksin* | Elefantit · Hautausmaa · Pelästynyt ihmisjoukossa |
| *Unessa* | Kuninkaat · Elokaupunki · Nuotio |
| *Coming soon...* | — |

↗ = the image links to a story page.

### Layout

- **Desktop:** a CSS grid of 250 px columns centred on the page. Size classes decide how much space an item takes: `.small`, `.large`, `.tall`, `.wide` and `.huge`. `.large` also scales the item up through the `--scale` custom property.
- **Hover:** the artwork lifts a little, grows 2 %, fades slightly, gets a soft shadow, and the cursor becomes a crosshair.
- **Mobile (≤ 768 px):** the grid becomes a wrapping flexbox of equal-sized tiles, three per row. Sections with two items show them side by side. Sections with three items show two on top and one centred below. The size classes are switched off at this width.
- Images use `loading="lazy"`.
- The font is **Inter**, loaded from Google Fonts.

### Page transitions

The inline script adds soft transitions between pages:

- **Fade in** when the page loads, and again when it is restored from the browser's back/forward cache (`pageshow`).
- **Fade out** (0.2 s) when a same-site `.html` link is clicked. The script then navigates to the link.
- `prefers-reduced-motion` turns off the body animation.

---

## Story pages — `stories/*.html`

All story pages share the same structure. They load `../style.css` and `../audio.js`.

```
← TAKAISIN TAIDEGALLERIAAN        (back link)
┌───────────────┐   Title
│               │   [ Uppoudu äänimaailmaan ]   (music button)
│    artwork    │   Story text…
│  + .ripple    │
└───────────────┘   Äänimaailma by me
```

| Page | Title | Image | Soundscape |
|---|---|---|---|
| `tuulenpuuska.html` | Tuulenpuuska | `tuulenpuuska.JPEG` | `garageband1_faded.mp3` (the first one made with GarageBand) |
| `cordoba-ilmapallo.html` | Vaikea valinta | `cordoban_ilmapallo_leikattu.JPEG` | `heavenly_loop_bandlab.mp3` |
| `eripintaiset-kasvot.html` | Kasvoja kadulla ja seinillä | `eripintaiset_naamat_leikattu.JPEG` | `bandlab_uniset_rummut_muokattu.mp3` |
| `frankenstein.html` | Frankenstein | `frankenstein_leikattu.JPEG` | `bandlab_eka_puhtaampi.mp3` |

On desktop, the image (600 px) and the text sit side by side, with the whole layout at most 1000 px wide. On mobile they stack, and the music button spans the full width.

### Audio feature — `audio.js`

Each story page has a music button that starts and stops looped playback of the page's mp3 file (`<audio id="background-music" loop>`). It works in any modern browser with HTML5 audio support.

- The button label switches between **"Uppoudu äänimaailmaan"** ("Immerse yourself in the soundscape") and **"Keskeytä kokemus"** ("Pause the experience").
- The script only runs when both the `#background-music` and `#music-toggle` elements exist on the page.

### Animation

Playing music starts an animation that looks like rain falling on the artwork:

- While music plays, `audio.js` adds a small `.pulse` circle every 200 ms. Each circle appears at a random spot inside the `.ripple` layer on top of the image.
- Each pulse grows and fades out over 2 s (`@keyframes pulseAnim` in `style.css`) and then removes itself.
- The `.story-image` container gets a `playing` class while music is on.

The plan is to develop this animation further later, possibly with ways for the viewer to interact with it.

### Back link

`← TAKAISIN TAIDEGALLERIAAN` points to `../index.html`. If the visitor arrived from this same site, `audio.js` uses `history.back()` instead. That way the gallery reopens where the visitor left it, and the fade-in plays again.

---

## Assets

- **`images/`**: photos of the artworks. Files ending in `_leikattu` ("cropped") are the cropped versions used on the site. The folder also has artworks that are not on the site yet, plus earlier versions of some images.
- **`audio/`**: original soundscapes, mostly made in **BandLab**, and since *Tuulenpuuska* also in **GarageBand**. The folder also keeps earlier drafts and mixes (`_kesken` = unfinished, `_faded`, `_mastered`, `_volumedown`, …).

Some file names contain Finnish letters (ä, ö). Links in the HTML must match these names exactly.

---

## Adding a new story

1. Add the artwork image to `images/` and the soundscape to `audio/`.
2. Copy `stories/template.html` to `stories/<new-name>.html`.
3. Fill in the placeholders: the `<title>`, the image `src` and `alt`, the `<h1>`, the audio `src` (it points to `../audio/music.mp3` by default), and the story text.
4. In `index.html`, wrap the artwork's `<img>` in a link to the new page, like this:
   ```html
   <div class="art-item large">
       <a href="stories/<new-name>.html">
           <img src="images/<image>.JPEG" alt="..." loading="lazy">
       </a>
   </div>
   ```

---

## Building the site — `build.py`

The text content and the list of drawings live in Markdown files in `content/`, and `build.py` turns them into the HTML pages. The Markdown files only say *what* is on the site; how it looks comes from the CSS and `templates/story.html`.

| You edit | The build writes |
|---|---|
| `content/gallery.md` | `index.html`: only the part between `<!-- GALLERY:START -->` and `<!-- GALLERY:END -->`, plus the page title |
| `content/stories/<name>.md` | `stories/<name>.html`, using the layout in `templates/story.html` |

Generated pages should not be edited by hand: the next build overwrites the changes.

### Using it

Run these in the terminal, from the project folder:

```bash
python3 build.py --dry-run   # show what would change, write nothing
python3 build.py             # build the site
```

1. Edit the Markdown files (e.g. in Typora).
2. Run `python3 build.py --dry-run` to see what would change. Optional, but useful when unsure.
3. Run `python3 build.py`.
4. Check the result in the browser (see *Running locally* below), then commit both the `.md` files and the generated `.html` files.

Nothing needs to be installed: the script only uses Python's standard library.

### Safety checks

Before writing anything, the build checks that every image, audio file and story mentioned in the Markdown files exists, with exactly the right spelling. This matters because macOS ignores differences in capital letters (`.JPEG` vs `.jpeg`) and in how ä/ö are stored, but GitHub Pages doesn't. A picture could work locally and be missing online.

If something is wrong, the build lists every problem with the file and line number, and **writes nothing**. For example:

```
Stopped: 1 problem(s) found. Nothing was written.

  - content/gallery.md, line 8: image not found: '../images/surullinen_kuu.jpeg' (the file is called 'surullinen_kuu.JPEG': check capital letters)
```

It also stops on things the story pages don't support yet (headings, lists, links or HTML in story text), so they can't end up looking out of place.

**Warnings** don't stop the build. They point out things worth checking, such as a gallery section with other than 2 or 3 drawings (the mobile layout is made for those).

### Markdown format

`content/gallery.md`:

```markdown
---
title: Matkalla
subtitle: © LAURI PRUDANT 2026
---

## Section name

![Name of drawing](../images/drawing.JPEG)
[![Name of drawing](../images/other.JPEG)](stories/story-name.md)
```

- The top block sets the page title and the line under it.
- `## ...` starts a section; a heading with no images is shown on its own (like *Coming soon...*).
- Each image line is one drawing; the name in `[...]` becomes the alt text. Wrapping it in a link to a story's `.md` file makes the tile open that story.
- Tile size is automatic: 3 drawings in a section → `large`, 2 → `huge`.

`content/stories/<name>.md`:

```markdown
---
title: Story title
audio: ../../audio/soundscape.mp3
---

![Name of drawing](../../images/drawing.JPEG)

First paragraph.

Second paragraph, with *italic* and **bold**.
```

- `title` is used for the page heading and the browser tab.
- The image line right below the top block is the story's drawing.
- A blank line starts a new paragraph.
- The file name becomes the page address: `tuulenpuuska.md` → `stories/tuulenpuuska.html`.

---

## Running locally

No installation is needed. Open `index.html` in a browser, or run a simple local server from the project folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Using a local server makes sure that the same-site page transitions and the back-link behaviour work the same way they do online.

---

## Repository

- Live site: [laurilaurilauri.github.io/matkalla](https://laurilaurilauri.github.io/matkalla/) (hosted on GitHub Pages)
- GitHub: [laurilaurilauri/matkalla](https://github.com/laurilaurilauri/matkalla)

© Lauri Prudant 2026
