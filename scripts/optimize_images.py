"""Resize images wider than MAX_W and re-save optimized, keeping name/format.
Usage: python3 -I optimize_images.py <src_dir> <dst_dir>
"""
import os, sys, shutil
from PIL import Image

MAX_W = 1600
src, dst = sys.argv[1], sys.argv[2]
before = after = 0
for root, _, files in os.walk(src):
    for name in files:
        s = os.path.join(root, name)
        d = os.path.join(dst, os.path.relpath(s, src))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        size = os.path.getsize(s)
        before += size
        try:
            im = Image.open(s)
            fmt = im.format
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            kw = {}
            if fmt == "JPEG":
                im = im.convert("RGB"); kw = dict(quality=82, optimize=True, progressive=True)
            elif fmt == "PNG":
                kw = dict(optimize=True)
            elif fmt == "WEBP":
                kw = dict(quality=82)
            im.save(d, fmt, **kw)
            if os.path.getsize(d) >= size and im.size == Image.open(s).size:
                shutil.copy2(s, d)  # no gain, keep original
        except Exception as e:
            print("copy-as-is", s, e)
            shutil.copy2(s, d)
        after += os.path.getsize(d)
print(f"{before/1e6:.0f} MB -> {after/1e6:.0f} MB")
