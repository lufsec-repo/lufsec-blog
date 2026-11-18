"""Convert a Ghost JSON export into Astro Markdown posts.

Usage: python3 -I convert.py <export.json> <out_dir> <image_list_out>
"""
import json, re, sys, os
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

SRC, OUT, IMGLIST = sys.argv[1], sys.argv[2], sys.argv[3]
SITE = "https://blog.lufsec.com"

data = json.load(open(SRC))["data"]
tags = {t["id"]: t for t in data["tags"]}
users = {u["id"]: u for u in data["users"]}
meta = {m["post_id"]: m for m in data["posts_meta"]}
post_tags = {}
for pt in sorted(data["posts_tags"], key=lambda x: x.get("sort_order") or 0):
    post_tags.setdefault(pt["post_id"], []).append(pt["tag_id"])
post_authors = {}
for pa in sorted(data["posts_authors"], key=lambda x: x.get("sort_order") or 0):
    post_authors.setdefault(pa["post_id"], []).append(pa["author_id"])

MALWARE = re.compile(r"_0x[0-9a-f]{4,}|gettingme\.info|\\x68\\x74\\x74\\x70")
images = set()
report = {"malware_stripped": [], "posts": 0}


def fix_url(u):
    if not u:
        return u
    u = u.replace("__GHOST_URL__", "")
    u = re.sub(r"^https?://blog\.lufsec\.com", "", u)
    # Ghost resized variants -> original
    u = re.sub(r"/content/images/size/w\d+(?:h\d+)?/(?:format/\w+/)?", "/content/images/", u)
    if u.startswith("/content/images/"):
        images.add(u.split("?")[0])
    return u


def yt_iframe(url):
    m = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{11})", url)
    if not m:
        return None
    return (f'<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
            'title="YouTube video" loading="lazy" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>')


class Conv(MarkdownConverter):
    def convert_img(self, el, text, parent_tags=None, **kw):
        src = fix_url(el.get("src", ""))
        alt = (el.get("alt") or "").replace("\n", " ").replace("]", "")
        return f"![{alt}]({src})"

    def convert_a(self, el, text, parent_tags=None, **kw):
        if el.get("href"):
            el["href"] = fix_url(el["href"])
        return super().convert_a(el, text, parent_tags=parent_tags, **kw)


def raw(soup, html):
    """Replace a node with a raw-HTML placeholder that survives markdownify."""
    key = f"RAWHTMLBLOCK{len(raw.store)}X"
    raw.store[key] = html
    return key
raw.store = {}


def clean_html(html, slug):
    soup = BeautifulSoup(html, "html.parser")
    stripped = False
    # 1. Malware: paragraphs/scripts containing the obfuscated dropper
    for el in soup.find_all(["p", "script", "div", "span"]):
        if el.parent is None:
            continue
        if MALWARE.search(el.get_text() or "") or (el.name == "script"):
            el.decompose(); stripped = True
    for s in soup.find_all(string=MALWARE):
        s.extract(); stripped = True
    if stripped:
        report["malware_stripped"].append(slug)
    # 2. Ghost signup cards (Ghost membership only)
    for el in soup.select(".kg-signup-card"):
        el.decompose()
    # 3. Embeds -> responsive iframes
    for el in soup.select(".kg-embed-card"):
        ifr = el.find("iframe")
        rep = None
        if ifr and ifr.get("src"):
            rep = yt_iframe(ifr["src"]) or f'<div class="embed">{ifr}</div>'
        else:
            rep = str(el)
        el.replace_with(raw(soup, rep))
    for ifr in soup.find_all("iframe"):
        rep = yt_iframe(ifr.get("src", "")) or f'<div class="embed">{ifr}</div>'
        ifr.replace_with(raw(soup, rep))
    # 4. WordPress leftovers: [embed]url[/embed] and Elementor junk
    for p in soup.find_all("p"):
        t = p.get_text().strip()
        m = re.fullmatch(r"\[embed\](.+?)\[/embed\]", t)
        if m:
            p.replace_with(raw(soup, yt_iframe(m.group(1)) or f'<p><a href="{m.group(1)}">{m.group(1)}</a></p>'))
    # 5. Button / CTA cards -> styled link
    for el in soup.select(".kg-button-card, .kg-cta-card"):
        a = el.find("a")
        txt_el = el.select_one(".kg-cta-text")
        lead = f"<p>{txt_el.get_text(' ', strip=True)}</p>" if txt_el else ""
        if a and a.get("href"):
            el.replace_with(raw(soup, f'<div class="cta">{lead}<a class="btn" href="{fix_url(a["href"])}">{a.get_text(strip=True) or "Learn more"}</a></div>'))
        else:
            el.decompose()
    # 6. Tables keep as HTML
    for t in soup.find_all("table"):
        t.replace_with(raw(soup, str(t)))
    # 7. Image cards: keep captions
    for fig in soup.select("figure.kg-image-card, figure"):
        img = fig.find("img")
        cap = fig.find("figcaption")
        if img:
            src = fix_url(img.get("src", ""))
            alt = (img.get("alt") or "").replace('"', "&quot;")
            capt = f"<figcaption>{cap.decode_contents()}</figcaption>" if cap else ""
            fig.replace_with(raw(soup, f'<figure><img src="{src}" alt="{alt}" loading="lazy" />{capt}</figure>'))
    return str(soup)


def to_md(html, slug):
    html = clean_html(html, slug)
    md = Conv(heading_style="ATX", bullets="-", code_language="", escape_underscores=False).convert(html)
    for k, v in raw.store.items():
        v = re.sub(r'(src|href)="([^"]+)"', lambda m: f'{m.group(1)}="{fix_url(m.group(2))}"', v)
        md = md.replace(k, f"\n\n{v}\n\n")
    raw.store.clear()
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return md


def yq(s):
    return json.dumps(s or "", ensure_ascii=False)


os.makedirs(OUT, exist_ok=True)
for p in data["posts"]:
    if p["type"] != "post" or p["status"] != "published":
        continue  # drafts, pages, and email-only ("sent") posts are skipped
    m = meta.get(p["id"], {})
    slug = p["slug"]
    t_names = [tags[t]["name"] for t in post_tags.get(p["id"], []) if t in tags and tags[t].get("visibility") == "public"]
    author = users.get((post_authors.get(p["id"]) or [None])[0], {}).get("name", "Luciano Ferrari")
    body = to_md(p.get("html") or "", slug)
    excerpt = p.get("custom_excerpt") or m.get("meta_description") or (p.get("plaintext") or "")
    excerpt = re.split(r"(?:function\s+)?_0x[0-9a-f]{4}", excerpt)[0]
    excerpt = re.sub(r"\[embed\].*?\[/embed\]", " ", excerpt)
    excerpt = re.sub(r"\s+", " ", excerpt).strip()[:300]
    fm = [
        "---",
        f"title: {yq(p['title'])}",
        f"slug: {yq(slug)}",
        f"pubDate: {p['published_at']}",
        f"updatedDate: {p['updated_at']}",
        f"author: {yq(author)}",
        f"description: {yq(excerpt)}",
        f"tags: {json.dumps(t_names, ensure_ascii=False)}",
        f"tagSlugs: {json.dumps([tags[t]['slug'] for t in post_tags.get(p['id'], []) if t in tags and tags[t].get('visibility') == 'public'])}",
        f"featured: {'true' if str(p.get('featured')) in ('1', 'True', 'true') else 'false'}",
    ]
    if p.get("feature_image"):
        fm.append(f"image: {yq(fix_url(p['feature_image']))}")
        if m.get("feature_image_alt"):
            fm.append(f"imageAlt: {yq(m['feature_image_alt'])}")
    if m.get("meta_title"):
        fm.append(f"metaTitle: {yq(m['meta_title'])}")
    if p.get("canonical_url"):
        fm.append(f"canonical: {yq(p['canonical_url'])}")
    fm.append("---")
    with open(os.path.join(OUT, f"{slug}.md"), "w") as f:
        f.write("\n".join(fm) + "\n\n" + body)
    report["posts"] += 1

s = {x["key"]: x["value"] for x in data["settings"]}
for k in ("logo", "icon", "cover_image"):
    fix_url(s.get(k))
with open(IMGLIST, "w") as f:
    f.write("\n".join(sorted(images)) + "\n")
print(json.dumps({"posts": report["posts"], "images": len(images),
                  "malware_stripped": len(report["malware_stripped"])}))
with open(os.path.join(os.path.dirname(IMGLIST), "malware-cleaned-posts.txt"), "w") as f:
    f.write("\n".join(report["malware_stripped"]) + "\n")
