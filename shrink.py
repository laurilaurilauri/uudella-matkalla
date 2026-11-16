#!/usr/bin/env python3
"""
Make the web versions of the drawings.

    python3 shrink.py

For each image in originals/, makes a copy in images/ for the website:
  - longer side over 2400 px: shrunk to 2400 px and saved as JPEG quality 85
  - 2400 px or less: copied as it is. Saving a small image again would only
    make the file bigger, without making it look better.
The copy keeps the original's name but always ends in .jpg
(e.g. originals/nuotio.JPEG -> images/nuotio.jpg). Originals are never changed.

An image is skipped if its copy in images/ is already newer than the original,
so running this again is quick, and an edited original is updated next time.

Uses the Mac's built-in sips tool. This file is the only part of the
site that needs changing if the site is ever built on Windows.
"""

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT / "originals"
IMAGES = ROOT / "images"

MAX_SIZE = 2400                                   # pixels, longer side
QUALITY = 85                                      # JPEG quality, 0-100
FORMATS = {".jpg", ".jpeg", ".png", ".heic"}      # capital letters are fine too


def longer_side(image):
    """The image's longer side in pixels, as reported by sips."""
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(image)],
                         capture_output=True, text=True, check=True).stdout
    return max(int(line.split()[-1]) for line in out.splitlines() if "pixel" in line)


def main():
    if not ORIGINALS.is_dir():
        print(f"No {ORIGINALS.name}/ folder found: nothing to do.")
        return
    made = 0
    for original in sorted(ORIGINALS.iterdir()):
        if original.suffix.lower() not in FORMATS:
            continue                              # e.g. .DS_Store
        web = IMAGES / (original.stem + ".jpg")
        if web.exists() and web.stat().st_mtime >= original.stat().st_mtime:
            continue                              # already up to date

        big = longer_side(original) > MAX_SIZE
        if not big and original.suffix.lower() in (".jpg", ".jpeg"):
            shutil.copy2(original, web)           # small JPEG: copy unchanged
            note = "copied as it is (already small)"
        else:
            # Big image: shrink. Small PNG/HEIC: only convert to JPEG.
            # (Without the size check, sips would also enlarge small images.)
            command = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(QUALITY)]
            if big:
                command += ["-Z", str(MAX_SIZE)]
            subprocess.run(command + [str(original), "--out", str(web)],
                           capture_output=True, check=True)
            note = "shrunk" if big else "converted to JPEG"

        print(f"{web.name}: {note}, {web.stat().st_size / 1_000_000:.2f} MB")
        made += 1

    print(f"{made} image(s) made." if made else "All images are up to date.")


if __name__ == "__main__":
    main()
