# Status

Where the site restructuring stands, so work can continue in a later session.
Background and ground rules are in CLAUDE.md. Lauri makes all commits himself.

*Last updated: 16 November 2026*

## Last completed

- Image compression tool: shrink.py makes the web-size images from the full-size ones in the new originals folder (which git ignores). Images over 2400 px are shrunk to 2400 px (JPEG quality 85); smaller ones are copied unchanged. The current images were moved to originals and the web copies made: the front page went from 20 MB to 10.9 MB, all images from 43.5 MB to 23 MB. README.md explains how to use it.
- Still to do by Lauri: check the site in the browser (images look sharp enough, nothing missing), then commit. build.py doesn't need to be run: the image names didn't change.

## Next actions: 

-  Visual tweaks:

  - A top bar that follows as the visitor scrolls down displaying "Matkalla"?

    - inspired from [Kansallisgalleria](https://kokoelma.kansallisgalleria.fi/en/) 


## Later

**Optional**:

- Change the page language setting from English to Finnish (own small commit)
- Build warnings, and a list of images and audio files the site doesn't use
- Run the build automatically on GitHub
- a Typora theme that looks like the site

## Decisions

- **Image and audio names without ä/ö, underscores or .JPEG.** The letters ä and ö can be stored in two different ways inside a file name, which caused mix-ups. Simple names are easier to type and work the same everywhere.
- **Image compression in its own script (shrink.py), not in build.py.** build.py stays short, and if the site is ever updated on Windows, only shrink.py needs changing. It only needs running after adding or changing an original.
- **Web images: max 2400 px, JPEG quality 85.** Tested 1600, 2000 and 2400 px; chose the sharpest, as it still roughly halves the size. Images of 2400 px or less are copied unchanged, because saving them again made 15 of 16 bigger.
- **Originals in the project's originals folder**, not read straight from iCloud: simpler, and works the same on Windows. Backed up in iCloud.
- **No naming check in build.py.** Considered a warning for badly named files, but left out: it's not essential, and checking names by eye is easy. build.py stays shorter.
- **Markdown and a small Python script.** Jekyll was considered, but it brings its own folder rules and template language, and the site would be harder to understand.
- **Front page file:** the top block holds the site title and copyright line. Each "##" heading is a gallery section; each image line is a drawing. A heading with no images is shown on its own (like "Coming soon...").
- **Story links** in the front page file point to the story's Markdown file, so they can be clicked in Typora. The script turns them into links to the web pages.
- **Story files:** the top block holds the title and the audio file. The drawing is an ordinary image line in the text, so Typora shows it while writing. The file name becomes the page address.
- **Formatting in stories:** paragraphs, italic and bold only. Other elements (subheadings, lists, links) are added when actually needed, each with styling Lauri approves – otherwise they would look out of place on the site.
- **Drawing sizes:** three drawings in a section are shown large, two are shown huge. Any other number: large, plus a warning, because the mobile layout only handles two or three.
- **No intro text** on the front page for now.
- **The script is written from scratch**; the earlier draft wasn't found.
- **Styling stays split** between the front page and the story pages. They look different, so this is fine. Front page: gallery.css and gallery.js. Story pages: style.css and audio.js.
- **Safety:** the script stops without changing anything if an image, audio file or story is missing or misspelled.
- **Audio is optional.** Not every drawing has a soundscape. A story without one leaves out the music button and the credit line instead of showing a button that does nothing.

## Good to know

- **README.md** has a step-by-step example of adding a new section and a story.

- **Image and audio names:** lowercase, hyphens between words, no ä/ö, ending in .jpg or .mp3. Example: *Jäätynyt järvi* → jaatynyt-jarvi.jpg. Capital letters matter online.
- **Typora theme "Matkalla":** shows images at half size while writing. It's based on Typora's default GitHub theme, so it's easy to tell apart from the theme used for other documents. Choose it from the Themes menu when working on the site. The file is matkalla.css in Typora's themes folder (Typora → Preferences → Appearance → Open Theme Folder). It's outside the project, so git doesn't track it. It didn't seem to work on the first try; still to be checked (first step: fully quit Typora with Cmd+Q and reopen).
