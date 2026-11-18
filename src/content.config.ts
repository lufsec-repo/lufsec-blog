import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const posts = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/posts',
    // Use the Ghost slug as the id so URLs stay identical
    generateId: ({ data, entry }) => (data.slug as string) ?? entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Luciano Ferrari'),
    description: z.string().default(''),
    tags: z.array(z.string()).default([]),
    tagSlugs: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    metaTitle: z.string().optional(),
    canonical: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { posts };
