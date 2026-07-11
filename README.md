# YET ANOTHER RAJ

A blog built with [`rajp152k/ssg`](https://github.com/rajp152k/ssg).

## Content

Posts are canvas directories:

```txt
content/posts/<slug>/
  post.json
  canvas.md
```

`canvas.md` contains the post. `post.json` declares its canvas panes and layout.

`.ssg/state.json` is versioned post metadata. It preserves each post's created and updated timestamps; do not edit it manually.

## Commands

Normal use runs the GitHub dependency pinned in `package-lock.json`:

```bash
npm install
npm run blog:new -- "Post title"
npm run blog:dev
npm run blog:build
npm run blog:check
```

SSG contributors can use the sibling checkout instead:

```bash
npm run blog:new:local -- "Post title"
npm run blog:dev:local
npm run blog:build:local
npm run blog:check:local
```

## Templates

[`ssg`](https://github.com/rajp152k/ssg) owns the canonical templates. Refresh this blog's copies after an SSG template update:

```bash
npm run blog:sync-templates
# or, when working on the sibling checkout:
npm run blog:sync-templates:local
```

Site identity belongs in `ssg.config.json`. Template behavior belongs upstream in `ssg`.

`CNAME` is copied into `public/` during `blog:check` for GitHub Pages.
