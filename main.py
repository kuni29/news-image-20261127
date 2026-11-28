#!/usr/bin/env python3
"""Entry point for this news-image submission.

The picture itself is already in the repository as entry.png: it was
rendered from design.html with headless Chrome while the entry was built.
This program only carries those exact bytes to the place the grader
reads them from, so running it twice yields a byte-identical file.
Nothing here draws, downloads, or changes the image.
"""

import hashlib
import os
import shutil
import sys


def beside_this_file(name):
    """Path of a file sitting next to this program in the repository."""
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, name)


def sha256_of(path):
    """Hex digest of a file, read in 1 MiB chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = beside_this_file("entry.png")
    destination = os.path.join("/output", "entry.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(source, destination)
    if sha256_of(source) != sha256_of(destination):
        print("entry.png did not reproduce byte for byte", file=sys.stderr)
        return 1
    size = os.path.getsize(destination)
    print("wrote %s (%d bytes, sha256 %s…)"
          % (destination, size, sha256_of(destination)[:12]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
