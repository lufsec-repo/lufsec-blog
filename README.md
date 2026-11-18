# LufSec Blog (blog.lufsec.com)

Static blog built with [Astro](https://astro.build), migrated from Ghost on 2026-11-18.
Hosted free on Cloudflare Pages.

- 339 posts migrated with the **same URLs** as Ghost (`/post-slug/`, `/tag/slug/`, `/page/2/`)
- Images in `public/content/images/` (same paths as Ghost; large ones converted to WebP with 301 redirects in `public/_redirects`)
- RSS at `/rss.xml` (old `/rss/` redirects), sitemap at `/sitemap-index.xml`
- Google Analytics `G-LP6ZQYG2VZ` carried over
- Theme matches www.lufsec.com (Montserrat/Inter, #00C2FF, same header/footer menus)
- Menus, course paths and the end-of-post CTA are all in `src/site.ts`

## Write a new post

Create `src/content/posts/my-new-post.md`:

```md
---
title: "My New Post"
slug: "my-new-post"
pubDate: 2026-11-20T09:00:00-05:00
description: "One or two sentences for Google and social cards."
tags: ["AI Security", "Prompt Injection"]
tagSlugs: ["ai-security", "prompt-injection"]
image: "/content/images/2026/11/my-cover.webp"
---

Your post in Markdown. Code blocks, tables, images, and YouTube embeds all work.
```

Put images in `public/content/images/2026/11/`. Commit and push: Cloudflare rebuilds the site in about a minute.

To keep a post unpublished, add `draft: true`.

## Run locally

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to dist/
```

## Deploy (one time)

1. Create a GitHub repo (e.g. `lucianoferrari/lufsec-blog`) and push this folder.
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick the repo.
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment variable: `NODE_VERSION` = `22`
3. After the first deploy, go to the project's **Custom domains** tab → add `blog.lufsec.com`.
   - If lufsec.com DNS is on Cloudflare, it adds the record for you.
   - If DNS is elsewhere, create a `CNAME` record: `blog` → `<project>.pages.dev` (replacing the current Ghost record).
4. Check a few old URLs, then cancel Ghost.

## Migration notes

- 79 older posts (mostly imported from the old WordPress site) contained an obfuscated
  JavaScript dropper pointing to `gettingme.info` (a known WordPress injection), rendered as
  visible text on Ghost. It was stripped during conversion; the list is in
  `scripts/malware-cleaned-posts.txt`.
- Skipped: 13 drafts, 1 draft page, 1 email-only post.
- Ghost member signup boxes were removed (not used).
