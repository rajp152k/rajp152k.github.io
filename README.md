# YET ANOTHER RAJ

Consumer site for the SSG in `../ssg`.

## Blogging

Posts live under `content/posts/` as canvas-style directories:

```txt
content/posts/my-post/
  post.json
  canvas.md
```

Local commands:

```bash
npm install
npm run blog:new -- "Post title"
npm run blog:dev
npm run blog:build
```

`CNAME` is preserved for GitHub Pages deployment.
