# Status

Where the site restructuring stands, so work can continue in a later session.
Background and ground rules are in CLAUDE.md. Lauri makes all commits himself.

*Last updated: 11 November 2026*

## Last completed

- ~~Front page styles and script moved out of index.html into their own files, gallery.css and gallery.js, like the story pages already use style.css and audio.js. index.html now holds only the page structure and the generated gallery. Looks and works exactly as before.~~

## Next: write content in Markdown, generate the HTML

The idea: all text and the list of drawings live in Markdown files written in Typora. A small Python script turns them into the same web pages the site has now. The Markdown files contain only content; how things look is decided by the CSS and the page template.

**Note:** the pages are now generated. Edit the Markdown files in content, then run the build; don't edit the story pages or the gallery part of index.html by hand.

**Next commit – instructions**

- [x] README.md rewritten for the new structure (done early, together with commit 1)
- [x] Update the structure description in CLAUDE.md (done early: removed the outdated file tree and step plan, which STATUS.md now covers)
- [x] README links point to this repo and its new address (decided: they'll work once the site is live)
- [x] README describes gallery.css and gallery.js

## Later

- Publish this repo on GitHub Pages (switched on; the first try failed because of a GitHub outage – check that https://laurilaurilauri.github.io/uudella-matkalla/ works)
- Write a first new story to try out the workflow
- Change the page language setting from English to Finnish (own small commit)
- Build warnings, and a list of images and audio files the site doesn't use
- Optional: run the build automatically on GitHub; a Typora theme that looks like the site
- Make adding images easier:
  - Get rid of the .JPEG file type and replace with .jpg
  - use hyphens in naming (`image-example`) instead of (`image_example`)
  - get rid of all ä & ö in the names
- When build.py functionality has been verified, an image compression tool:
  - When `build.py` runs, it first checks the `originals/` folder, where the full-size JPEGs straight from the camera or scanner are kept. This folder is ignored by Git, so these large files never go to GitHub. For each original, the script checks whether `images/` already has a web version with the same file name that is newer than the original. If one is missing or out of date, it uses macOS’s built-in `sips` tool to make a smaller copy, at most 1600 px on the long side and saved as a moderately compressed JPEG (about 150–300 KB), and saves it in `images/`. The original is never changed. 
  - Images that are already up to date are skipped, so repeat builds are fast, and replacing an original with an edited version automatically updates its web copy on the next build. `gallery.md` and the story files always refer to the web versions in `images/`, and the site only ever uses those. Adding a new drawing therefore means putting the original in `originals/`, writing its line in Markdown, and running `python3 build.py`.

## Decisions

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

## Good to know

- **README.md** has a step-by-step example of adding a new section and a story.

- The letters ä and ö can be stored in two different ways inside a file name. A Mac treats both as the same name, and git on a Mac does too, so a git command can hit the wrong file. Check the result carefully when working with such file names.
- **Typora theme "Matkalla":** shows images at half size while writing. It's based on Typora's default GitHub theme, so it's easy to tell apart from the theme used for other documents. Choose it from the Themes menu when working on the site. The file is matkalla.css in Typora's themes folder (Typora → Preferences → Appearance → Open Theme Folder). It's outside the project, so git doesn't track it. It didn't seem to work on the first try; still to be checked (first step: fully quit Typora with Cmd+Q and reopen).
