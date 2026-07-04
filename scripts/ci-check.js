const fs = require('fs');
const path = require('path');

const checks = [];

function fail(message) {
  console.error(`[check failed] ${message}`);
  process.exit(1);
}

function ok(message) {
  checks.push(message);
}

function assertFile(filePath) {
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    fail(`missing required file: ${filePath}`);
  }
  ok(`${filePath} exists`);
}

function assertDir(dirPath) {
  if (!fs.existsSync(dirPath) || !fs.statSync(dirPath).isDirectory()) {
    fail(`missing required directory: ${dirPath}`);
  }
  ok(`${dirPath} exists`);
}

assertFile('CNAME');
if (fs.readFileSync('CNAME', 'utf8').trim() !== 'yetanotherraj.com') {
  fail('CNAME must contain yetanotherraj.com');
}
ok('CNAME points to yetanotherraj.com');

assertFile('package.json');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
for (const script of ['blog:build', 'blog:dev', 'blog:new', 'blog:check']) {
  if (!pkg.scripts || typeof pkg.scripts[script] !== 'string') {
    fail(`package.json must define ${script}`);
  }
}
ok('blogging scripts are present');

assertFile('ssg.config.json');
const config = JSON.parse(fs.readFileSync('ssg.config.json', 'utf8'));
if (config.paths?.postsDir !== 'content/posts') {
  fail('ssg.config.json must use content/posts as postsDir');
}
ok('SSG config points at content/posts');

assertDir('content/posts');
assertFile('templates/index.html');
assertFile('templates/post.html');
assertFile('templates/themes/light.css');
assertFile('templates/fonts/terminess.css');
assertFile('.ssg/state.json');

const postDirs = fs.readdirSync('content/posts')
  .map((name) => path.join('content/posts', name))
  .filter((entry) => fs.statSync(entry).isDirectory());

if (postDirs.length === 0) {
  fail('content/posts must contain at least one canvas post directory');
}

for (const postDir of postDirs) {
  assertFile(path.join(postDir, 'post.json'));
  assertFile(path.join(postDir, 'canvas.md'));
}
ok('all posts are canvas-style directories');

console.log('Blog CI checks passed:', checks.join(', '));
