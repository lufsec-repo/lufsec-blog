import { getCollection } from 'astro:content';

export async function getPosts() {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

// Ghost-style pagination: page 1 at the base, then /page/2/, /page/3/ …
export function paginate<T>(items: T[], perPage: number, base: string) {
  const last = Math.max(1, Math.ceil(items.length / perPage));
  return Array.from({ length: last }, (_, i) => {
    const n = i + 1;
    const url = (p: number) => (p === 1 ? base : `${base}page/${p}/`);
    return {
      n,
      items: items.slice(i * perPage, n * perPage),
      current: n,
      last,
      prev: n > 1 ? url(n - 1) : undefined,
      next: n < last ? url(n + 1) : undefined,
    };
  });
}
