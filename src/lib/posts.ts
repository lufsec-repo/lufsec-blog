import { getCollection } from 'astro:content';

export async function getPosts() {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

// Ghost-style pagination: page 1 at the base, then /page/2/, /page/3/ …
// firstPage lets the homepage show one extra post (the large "latest" card + a full grid).
export function paginate<T>(items: T[], perPage: number, base: string, firstPage = perPage) {
  const rest = Math.max(0, items.length - firstPage);
  const last = 1 + Math.ceil(rest / perPage);
  return Array.from({ length: last }, (_, i) => {
    const n = i + 1;
    const url = (p: number) => (p === 1 ? base : `${base}page/${p}/`);
    const start = i === 0 ? 0 : firstPage + (i - 1) * perPage;
    const end = i === 0 ? firstPage : start + perPage;
    return {
      n,
      items: items.slice(start, end),
      current: n,
      last,
      prev: n > 1 ? url(n - 1) : undefined,
      next: n < last ? url(n + 1) : undefined,
    };
  });
}
