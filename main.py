#!/usr/bin/env python3
"""news-image-20261127: emit the finished front page as entry.png.

The picture itself is drawn once, by hand, in design.html and rendered to
entry.png with headless Chrome (render.mjs). This program does no drawing:
it only places that exact file where the grader expects it, byte for byte,
every time it runs. Determinism is the whole job here, so the copy is done
through a single read of the committed bytes and a single write to the
output directory, with a hash printed so a repeated run can be compared.
"""

import hashlib
import os
import pathlib
import sys

SOURCE_NAME = "entry.png"


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent


def output_dir() -> pathlib.Path:
    chosen = os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT")
    if chosen:
        return pathlib.Path(chosen)
    return pathlib.Path("/output")


def sha256_hex(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def main() -> int:
    source = repo_root() / SOURCE_NAME
    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 1
    payload = source.read_bytes()
    if len(payload) == 0 or len(payload) > 1_048_576:
        print(f"bad source size: {len(payload)} bytes", file=sys.stderr)
        return 1
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        print("source is not a PNG file", file=sys.stderr)
        return 1
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE_NAME
    with open(target, "wb") as handle:
        handle.write(payload)
    written = target.read_bytes()
    if written != payload:
        print("round-trip mismatch after writing entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(payload)} bytes, sha256 {sha256_hex(payload)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
