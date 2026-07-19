# YET ANOTHER RAJ

A blog built with [`rajp152k/ssg`](https://github.com/rajp152k/ssg).

## Content

Posts are canvas directories:

```txt
content/posts/<slug>/
  post.json
  canvas.md
```

`canvas.md` contains the post. `post.json` declares its creation time, canvas
panes, and layout. `blog:new` writes `createdAt` once; authors do not maintain
it manually.

Meditations are plain Markdown files under `content/meditations/`. They use
only `title` and `date` front matter, appear newest-first under `/meditations/`,
and are paginated after 20 entries.

## Commands

Normal use runs the GitHub dependency pinned in `package-lock.json`:

```bash
npm install
npm run blog:new -- "Post title"
npm run blog:new:meditation -- "Meditation title"
npm run blog:dev
npm run blog:build
npm run blog:check
```

## Templates

[`ssg`](https://github.com/rajp152k/ssg) owns the canonical templates. Refresh this blog's copies after an SSG template update:

```bash
npm run blog:sync-templates
# explicitly copy templates from a sibling SSG checkout:
npm run blog:sync-templates:local
```

Site identity belongs in `ssg.config.json`. Template behavior belongs upstream in `ssg`.

`CNAME` is copied into `public/` during `blog:check` for GitHub Pages.
