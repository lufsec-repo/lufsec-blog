"""Convert large images to WebP, rewrite Markdown references, emit redirects.
Usage: python3 -I webpify.py <site_dir> <min_kb>
"""
import os, re, sys
from PIL import Image

site, min_kb = sys.argv[1], int(sys.argv[2])
img_root = os.path.join(site, "public")
posts = os.path.join(site, "src", "content", "posts")
mapping = {}
for root, _, files in os.walk(os.path.join(img_root, "content", "images")):
    for name in files:
        p = os.path.join(root, name)
        base, ext = os.path.splitext(name)
        if ext.lower() not in (".png", ".jpg", ".jpeg") or os.path.getsize(p) < min_kb * 1024:
            continue
        new = os.path.join(root, base + ".webp")
        if os.path.exists(new):
            new = os.path.join(root, base + "-" + ext.lstrip(".").lower() + ".webp")
        im = Image.open(p)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "transparency" in im.info or im.mode in ("LA", "P") else "RGB")
        im.save(new, "WEBP", quality=80, method=6)
        os.remove(p)
        old_url = "/" + os.path.relpath(p, img_root)
        mapping[old_url] = "/" + os.path.relpath(new, img_root)

n_files = 0
for name in os.listdir(posts):
    fp = os.path.join(posts, name)
    txt = open(fp).read()
    new_txt = txt
    for old, new in mapping.items():
        new_txt = new_txt.replace(old, new)
    if new_txt != txt:
        open(fp, "w").write(new_txt); n_files += 1

with open(os.path.join(img_root, "_redirects"), "a") as f:
    f.write("\n# Images converted to WebP during migration\n")
    for old, new in sorted(mapping.items()):
        f.write(f"{old.replace(' ', '%20')}  {new.replace(' ', '%20')}  301\n")
print(f"converted {len(mapping)} images, updated {n_files} posts")
