# Status

Where the site restructuring stands, so work can continue in a later session.
Background and ground rules are in CLAUDE.md. Lauri makes all commits himself.

*Last updated: 11 November 2026*

## Last completed

- ~~Commit 1, content and build script: the gallery and the four stories as Markdown, the story page template, build.py with a dry-run mode, the two markers in index.html, and a build guide in README.md. A dry run showed the generated pages match the current ones, apart from spacing and two explanatory comments.~~

## Next: write content in Markdown, generate the HTML

The idea: all text and the list of drawings live in Markdown files written in Typora. A small Python script turns them into the same web pages the site has now. The Markdown files contain only content; how things look is decided by the CSS and the page template.

**Note:** the site still runs on the old hand-made HTML. The build has only been run as a dry run, so editing the Markdown files has no effect yet. That changes with commit 2.

**Commit 2 – regenerate the pages**

- [ ] Run the build script, which rewrites the gallery part of index.html and the four story pages
- [ ] Remove the old stories/template.html (replaced by the new template)
- [ ] Check that nothing changed except spacing, and click through the site locally

**Commit 3 – instructions**

- [x] README.md rewritten for the new structure (done early, together with commit 1)
- [x] Update the structure description in CLAUDE.md (done early: removed the outdated file tree and step plan, which STATUS.md now covers)
- [ ] Decide whether the README links should point to this repo instead of the original one

## Later

- Change the page language setting from English to Finnish (own small commit)
- Build warnings, and a list of images and audio files the site doesn't use
- Optional: move the front page styles into their own file; run the build automatically on GitHub; a Typora theme that looks like the site

## Decisions

- **Markdown and a small Python script.** Jekyll was considered, but it brings its own folder rules and template language, and the site would be harder to understand.
- **Front page file:** the top block holds the site title and copyright line. Each "##" heading is a gallery section; each image line is a drawing. A heading with no images is shown on its own (like "Coming soon...").
- **Story links** in the front page file point to the story's Markdown file, so they can be clicked in Typora. The script turns them into links to the web pages.
- **Story files:** the top block holds the title and the audio file. The drawing is an ordinary image line in the text, so Typora shows it while writing. The file name becomes the page address.
- **Formatting in stories:** paragraphs, italic and bold only. Other elements (subheadings, lists, links) are added when actually needed, each with styling Lauri approves – otherwise they would look out of place on the site.
- **Drawing sizes:** three drawings in a section are shown large, two are shown huge. Any other number: large, plus a warning, because the mobile layout only handles two or three.
- **No intro text** on the front page for now.
- **The script is written from scratch**; the earlier draft wasn't found.
- **Styling stays split** between the front page and the story pages. They look different, so this is fine.
- **Safety:** the script stops without changing anything if an image, audio file or story is missing or misspelled.

## Good to know

- The letters ä and ö can be stored in two different ways inside a file name. A Mac treats both as the same name, and git on a Mac does too, so a git command can hit the wrong file. Check the result carefully when working with such file names.
- **Typora theme "Matkalla":** shows images at half size while writing. It's based on Typora's default GitHub theme, so it's easy to tell apart from the theme used for other documents. Choose it from the Themes menu when working on the site. The file is matkalla.css in Typora's themes folder (Typora → Preferences → Appearance → Open Theme Folder). It's outside the project, so git doesn't track it. It didn't seem to work on the first try; still to be checked (first step: fully quit Typora with Cmd+Q and reopen).
