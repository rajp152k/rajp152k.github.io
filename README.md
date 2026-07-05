# YET ANOTHER RAJ

Consumer site for the SSG in `../ssg`.

## Blogging

Posts live under `content/posts/` as canvas-style directories:

```txt
content/posts/my-post/
  post.json
  canvas.md
```

Local commands using the Git dependency:

```bash
npm install
npm run blog:new -- "Post title"
npm run blog:dev
npm run blog:build
```

When iterating on the sibling SSG checkout, use the local scripts instead:

```bash
npm run blog:new:local -- "Post title"
npm run blog:dev:local
npm run blog:build:local
```

Templates are copied into this repo so site-specific edits remain possible. To refresh them from the installed Git dependency:

```bash
npm run blog:sync-templates
```

When iterating against the sibling SSG checkout, sync from there instead:

```bash
npm run blog:sync-templates:local
```

`CNAME` is preserved for GitHub Pages deployment.
