import rss from '@astrojs/rss';
import { getPosts } from '../lib/posts';
import { SITE } from '../site';

export async function GET(context) {
  const posts = await getPosts();
  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site,
    trailingSlash: true,
    items: posts.slice(0, 50).map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/${post.id}/`,
      categories: post.data.tags,
    })),
  });
}
