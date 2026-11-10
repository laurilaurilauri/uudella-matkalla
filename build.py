#!/usr/bin/env python3
"""
Build the website from the Markdown files in content/.

    python3 build.py            build the site (writes index.html and stories/*.html)
    python3 build.py --dry-run  only show what would change; writes nothing

What it does:
  1. Reads content/gallery.md and every content/stories/*.md file.
  2. Checks the Markdown files against the real files in the project folder
     and against the agreed format. The build stops if:
       - an image, audio file or story it mentions doesn't exist exactly as
         written: same spelling, same capital letters, and ä/ö stored the
         normal way (otherwise it may work on a Mac but break on GitHub)
       - a required setting in the top block is missing or misspelled
         (e.g. a story without "title:" or "audio:")
       - a line doesn't follow the format (in gallery.md only "## Section"
         and image lines; in stories no headings, lists, links or HTML yet)
     It then lists every problem with file and line number, and writes NOTHING.
  3. Writes the pages:
       - index.html: only the part between <!-- GALLERY:START --> and
         <!-- GALLERY:END -->, plus the page title. Styles and scripts in
         index.html are never touched.
       - stories/<name>.html: one page per content/stories/<name>.md,
         using the layout in templates/story.html.

Uses only Python's standard library, so nothing needs to be installed.
"""

import difflib
import html
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

# --- Where things are ------------------------------------------------------

ROOT = Path(__file__).resolve().parent          # the project folder
CONTENT = ROOT / "content"
GALLERY_MD = CONTENT / "gallery.md"
STORIES_MD = CONTENT / "stories"
STORY_TEMPLATE = ROOT / "templates" / "story.html"
INDEX_HTML = ROOT / "index.html"
STORIES_HTML = ROOT / "stories"

START_MARKER = "<!-- GALLERY:START -->"
END_MARKER = "<!-- GALLERY:END -->"

# Tile size by number of drawings in a section. Other counts get "large"
# and a warning, because the mobile layout only has rules for 2 and 3.
TILE_SIZES = {2: "huge", 3: "large"}
DEFAULT_TILE_SIZE = "large"

# --- Collecting problems ---------------------------------------------------
# Errors stop the build (nothing is written). Warnings are only shown.

errors = []
warnings = []


def error(source, line_no, message):
    errors.append(f"{where(source, line_no)}: {message}")


def warn(source, line_no, message):
    warnings.append(f"{where(source, line_no)}: {message}")


def where(path, line_no):
    """Turn a file path and line number into e.g. 'content/gallery.md, line 9'."""
    text = rel(path)
    return f"{text}, line {line_no}" if line_no else text


def rel(path):
    """A path relative to the project folder, with forward slashes."""
    return Path(os.path.relpath(path, ROOT)).as_posix()


# --- Reading Markdown files ------------------------------------------------

def read_text(path):
    """Read a file as text. Letters like ä are normalised to their usual
    one-character form, so file names written in the text match the files."""
    return unicodedata.normalize("NFC", path.read_text(encoding="utf-8"))


def split_front_matter(path, allowed_keys, required_keys):
    """
    Split a Markdown file into its top block (between the two --- lines)
    and the rest. Returns (settings, body_lines), where body_lines is a list
    of (line_number, text) pairs.
    """
    lines = read_text(path).splitlines()
    settings = {}

    if not lines or lines[0].strip() != "---":
        error(path, 1, "the file must start with a top block between two --- lines")
        return settings, []

    # Find the closing --- line.
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        error(path, 1, "the top block is missing its closing --- line")
        return settings, []

    for i in range(1, end):
        line = lines[i].strip()
        if not line:
            continue
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if not sep or key not in allowed_keys:
            error(path, i + 1, f"unknown setting '{line}' (allowed: {', '.join(allowed_keys)})")
            continue
        settings[key] = value

    for key in required_keys:
        if not settings.get(key):
            error(path, 1, f"the top block is missing '{key}:'")

    body = [(i + 1, lines[i]) for i in range(end + 1, len(lines))]
    return settings, body


# Patterns for image lines:
#   ![Name](path)                 an image
#   [![Name](path)](story.md)     an image that links to a story
IMAGE = r"!\[([^\]]*)\]\(([^)\s]+)\)"
IMAGE_LINE = re.compile(rf"^{IMAGE}$")
LINKED_IMAGE_LINE = re.compile(rf"^\[{IMAGE}\]\(([^)\s]+)\)$")


# --- Checking that files exist (spelling-safe) -----------------------------

def find_file(md_file, line_no, link, kind):
    """
    Resolve a link written in a Markdown file (e.g. '../images/x.JPEG') and
    check that the file exists with exactly that spelling.

    Why not just Path.exists()? On a Mac, 'X.jpeg' and 'x.JPEG' count as
    the same file, but on GitHub Pages they don't, so a picture could work
    locally and be missing on the website. So each part of the path is
    compared letter by letter with the real names in the folder.

    Returns the full path, or None if there's a problem (and records an error).
    """
    link = unicodedata.normalize("NFC", unquote(link))   # Typora may write ä as %C3%A4
    target = Path(os.path.normpath(md_file.parent / link))

    try:
        parts = target.relative_to(ROOT).parts
    except ValueError:
        error(md_file, line_no, f"{kind} '{link}' points outside the project folder")
        return None

    folder = ROOT
    for part in parts:
        names = os.listdir(folder) if folder.is_dir() else []
        if part in names:
            folder = folder / part
            continue

        # Not found with exact spelling: look for a near miss to give a hint.
        hint = ""
        for name in names:
            if name.lower() == part.lower():
                hint = f" (the file is called '{name}': check capital letters)"
            elif unicodedata.normalize("NFC", name) == part:
                hint = (f" (a file '{part}' exists, but its ä/ö is stored in an unusual way "
                        f"that the website can't find; rename the file and type the name again)")
        error(md_file, line_no, f"{kind} not found: '{link}'{hint}")
        return None

    return target


def link_from(output_file, target):
    """The link to use inside output_file to reach target, e.g. '../images/x.JPEG'."""
    return Path(os.path.relpath(target, output_file.parent)).as_posix()


# --- Story text: paragraphs, *italic* and **bold** -------------------------

def format_paragraph(md_file, line_no, text):
    """Turn one paragraph of Markdown text into HTML (escaped, with em/strong)."""
    # Things that aren't supported yet. They'd look out of place on the site
    # without matching styling, so stop with a clear message instead.
    if re.match(r"^#", text):
        error(md_file, line_no, "headings aren't supported in story text yet")
    elif re.match(r"^([-+*]|\d+\.)\s", text):
        error(md_file, line_no, "lists aren't supported in story text yet")
    elif text.startswith(">"):
        error(md_file, line_no, "quotes aren't supported in story text yet")
    elif "](" in text:
        error(md_file, line_no, "links and extra images aren't supported in story text yet")
    elif re.search(r"<[a-zA-Z/!]", text):
        error(md_file, line_no, "HTML isn't supported in story text")

    text = html.escape(text, quote=False)                                 # & < > shown as text
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)        # **bold**
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)                    # *italic*
    if "*" in text:
        error(md_file, line_no, "a * without its pair (use *italic* or **bold**)")
    return text


# --- Building a story page -------------------------------------------------

def build_story(md_file, template):
    """Return (output_path, html) for one content/stories/<name>.md file."""
    output = STORIES_HTML / (md_file.stem + ".html")
    settings, body = split_front_matter(md_file, ["title", "audio"], ["title", "audio"])

    image = alt = None
    paragraphs = []        # list of (first_line_number, [lines])
    current = None

    for line_no, line in body:
        text = line.strip()
        if not text:                         # a blank line ends a paragraph
            current = None
            continue
        match = IMAGE_LINE.match(text)
        if match and image is None and not paragraphs:
            # The story's drawing: an image line before the text starts.
            alt, image_link = match.groups()
            image = find_file(md_file, line_no, image_link, "image")
            if image is None:
                image = False                # remember there was one, but it's broken
            continue
        if current is None:                  # start a new paragraph
            current = (line_no, [])
            paragraphs.append(current)
        current[1].append(text)

    if image is None:
        error(md_file, None, "no drawing found: put an image line like "
                             "![Name](../../images/x.JPEG) right below the top block")
    if not paragraphs:
        warn(md_file, None, "the story has no text")

    audio = find_file(md_file, None, settings["audio"], "audio") if settings.get("audio") else None

    # Lines inside one paragraph are joined with a space. Paragraphs are
    # separated with <br> <br>, the same way as in the original pages.
    body_html = "\n            <br> <br>".join(
        format_paragraph(md_file, first_line, " ".join(lines)) for first_line, lines in paragraphs
    )

    if not (image and audio and settings.get("title")):
        return output, None                  # errors already recorded

    values = {
        "title": html.escape(settings["title"]),
        "image": link_from(output, image),
        "alt": html.escape(alt),
        "audio": link_from(output, audio),
        "body": body_html,
    }
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), m.group(0)), template)
    leftover = re.search(r"\{\{\w+\}\}", page)
    if leftover:
        error(STORY_TEMPLATE, None, f"unknown placeholder {leftover.group(0)}")
    return output, page


# --- Building the gallery (front page) -------------------------------------

def tile_html(size, image_src, alt, story_href=None):
    """HTML for one drawing in the gallery."""
    img = f'<img src="{image_src}" alt="{html.escape(alt)}" loading="lazy">'
    if story_href is None:
        return f'        <div class="art-item {size}">{img}</div>'
    return (f'        <div class="art-item {size}">\n'
            f'            <a href="{story_href}">\n'
            f'                {img}\n'
            f'            </a>\n'
            f'        </div>')


def build_gallery():
    """Return (site_title, html_block) for the part of index.html between the markers."""
    settings, body = split_front_matter(GALLERY_MD, ["title", "subtitle"], ["title"])

    # First collect sections: each is [heading, line_no, [tiles]], where a
    # tile is (image_src, alt, story_href or None).
    sections = []
    for line_no, line in body:
        text = line.strip()
        if not text:
            continue

        if text.startswith("## "):
            sections.append([text[3:].strip(), line_no, []])
            continue

        linked = LINKED_IMAGE_LINE.match(text)
        plain = IMAGE_LINE.match(text)
        if not (linked or plain):
            error(GALLERY_MD, line_no, f"not understood: '{text}' "
                                       "(expected '## Section' or an image line)")
            continue
        if not sections:
            error(GALLERY_MD, line_no, "image before the first ## section heading")
            continue

        alt, image_link = (linked or plain).groups()[:2]
        image = find_file(GALLERY_MD, line_no, image_link, "image")
        story_href = None
        if linked:
            story = find_file(GALLERY_MD, line_no, linked.group(3), "story")
            if story is not None:
                if story.suffix != ".md" or story.parent != STORIES_MD:
                    error(GALLERY_MD, line_no, "a story link must point to a .md file in content/stories/")
                else:
                    story_href = link_from(INDEX_HTML, STORIES_HTML / (story.stem + ".html"))
        if image is not None:
            sections[-1][2].append((link_from(INDEX_HTML, image), alt, story_href))

    # Then turn the sections into HTML, laid out like the original index.html.
    out = ["    " + START_MARKER,
           "    <!-- Generated by build.py from content/gallery.md. Edit that file, not this part. -->",
           "    <header>",
           f"        <h1>{html.escape(settings.get('title', ''))}</h1>"]
    if settings.get("subtitle"):
        out.append(f"        <p><em>{html.escape(settings['subtitle'])}</em></p>")
    out.append("    </header>")

    for heading, line_no, tiles in sections:
        out += ["", f'    <div class="text-break"><em>{html.escape(heading)}</em></div>']
        if not tiles:
            continue                         # heading only, e.g. "Coming soon..."
        size = TILE_SIZES.get(len(tiles), DEFAULT_TILE_SIZE)
        if len(tiles) not in TILE_SIZES:
            warn(GALLERY_MD, line_no, f"section '{heading}' has {len(tiles)} drawings; "
                                      "the mobile layout is made for 2 or 3, so check how it looks")
        out += ["", '    <div class="gallery">']
        out += [tile_html(size, *tile) for tile in tiles]
        out.append("    </div>")

    out.append("    " + END_MARKER)
    return settings.get("title", ""), "\n".join(out)


def update_index(site_title, gallery_block):
    """Return the new index.html text: the marked block and <title> replaced."""
    text = INDEX_HTML.read_text(encoding="utf-8")
    start, end = text.find(START_MARKER), text.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        error(INDEX_HTML, None, f"couldn't find the {START_MARKER} and {END_MARKER} lines")
        return None

    # Replace from the start of the START line to the end of the END marker.
    start = text.rfind("\n", 0, start) + 1
    end += len(END_MARKER)
    text = text[:start] + gallery_block + text[end:]

    text, count = re.subn(r"<title>.*?</title>", f"<title>{html.escape(site_title)}</title>", text, count=1)
    if count == 0:
        error(INDEX_HTML, None, "couldn't find the <title> line")
    return text


# --- Main ------------------------------------------------------------------

def main():
    # Only "--dry-run" is allowed. Anything else (e.g. a typo like "--dryrun")
    # stops here, so a mistyped dry run never turns into a real build.
    args = sys.argv[1:]
    if any(arg != "--dry-run" for arg in args):
        print("Usage: python3 build.py [--dry-run]")
        sys.exit(2)
    dry_run = "--dry-run" in args

    # 1. Build everything in memory first.
    outputs = {}                                     # output path -> new text
    template = STORY_TEMPLATE.read_text(encoding="utf-8")
    story_files = sorted(STORIES_MD.glob("*.md"))
    for md_file in story_files:
        output, page = build_story(md_file, template)
        if page is not None:
            outputs[output] = page

    site_title, block = build_gallery()
    index = update_index(site_title, block)
    if index is not None:
        outputs[INDEX_HTML] = index

    # Story pages that no longer have a Markdown file are left alone, but mentioned.
    sources = {f.stem for f in story_files}
    for page in sorted(STORIES_HTML.glob("*.html")):
        if page.stem not in sources:
            warn(page, None, "has no matching .md file in content/stories/ (not changed by the build)")

    for message in warnings:
        print("Warning:", message)

    # 2. If anything was wrong, stop before writing.
    if errors:
        print(f"\nStopped: {len(errors)} problem(s) found. Nothing was written.\n")
        for message in errors:
            print("  -", message)
        sys.exit(1)

    # 3. Write (or, in a dry run, show) only the files that change.
    changed = []                                     # (file name, note) per changed file
    for path, new in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if new == old:
            continue
        only_spacing = re.sub(r"\s+", "", old) == re.sub(r"\s+", "", new)
        note = " (only spacing changes)" if only_spacing else ""
        changed.append((rel(path), note))
        if dry_run:
            print(f"\n=== {rel(path)} would change{note} ===")
            sys.stdout.writelines(difflib.unified_diff(
                old.splitlines(keepends=True), new.splitlines(keepends=True),
                fromfile=f"{rel(path)} (now)", tofile=f"{rel(path)} (after build)"))
        else:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(f"Updated {rel(path)}{note}")

    if not changed:
        print("Everything is up to date.")
    elif dry_run:
        print(f"\nDry run: {len(changed)} file(s) would change. Nothing was written.")
        for name, note in changed:
            print(f"  - {name}{note}")


if __name__ == "__main__":
    main()
