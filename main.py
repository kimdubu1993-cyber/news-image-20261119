"""news-image-20261119 entry.

Copies the pre-rendered front page (news.png) byte-for-byte to the
output directory as entry.png, then verifies the copy matches the
source in size and SHA-256.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    src_size = os.path.getsize(SOURCE)
    dst_size = os.path.getsize(dest)
    if src_size != dst_size:
        print(
            f"error: size mismatch: source {src_size} bytes, "
            f"copy {dst_size} bytes",
            file=sys.stderr,
        )
        return 1
    src_hash = sha256_of(SOURCE)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print(
            "error: SHA-256 mismatch between news.png and entry.png",
            file=sys.stderr,
        )
        return 1
    print(f"copied news.png -> {dest} ({dst_size} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
