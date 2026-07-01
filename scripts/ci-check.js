const fs = require('fs');

const checks = [];

function fail(message) {
  console.error(`[check failed] ${message}`);
  process.exit(1);
}

function ok(message) {
  checks.push(message);
}

const readme = fs.readFileSync('README.md', 'utf8');
if (!readme.trim().startsWith('# yet another raj')) {
  fail('README.md must start with `# yet another raj`');
}
ok('README exists and has expected title');

const workflow = fs.readFileSync('.github/workflows/deploy-readme.yml', 'utf8');
if (!workflow.includes('actions/deploy-pages@v4')) {
  fail('deploy workflow must use actions/deploy-pages@v4');
}
ok('Deploy workflow includes GitHub Pages deployment action');

if (!workflow.includes('pages: write')) {
  fail('deploy workflow should include pages write permission');
}
ok('Deploy workflow has pages write permission');

const branch = 'master';
if (!workflow.includes(`  branches:\n    - ${branch}`) && !workflow.includes(`- ${branch}`)) {
  fail('deploy workflow should target master branch');
}
ok('Deploy workflow targets expected branch');

console.log('Blog CI checks passed:', checks.join(', '));
