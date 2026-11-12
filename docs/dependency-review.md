# Dependency review

Review date: 2026-11-12. Scope: npm dependencies used for local assets.

## Findings and change

The initial `npm audit --json` reported three affected packages: one critical
and two low. DOMPurify 3.4.16 had critical, high, and low advisories. KaTeX
0.16.47 had a low advisory; npm also reported Mermaid 12.1.0 as affected through
KaTeX.

Upgrade Mermaid to 12.2.0, the next minor release. Its supported KaTeX range is
`^0.18.0`, which permits the fixed release. Update DOMPurify within Mermaid's
existing `^3.4.12` range. The lock file now selects:

| Package | Before | After |
| --- | --- | --- |
| Mermaid | 12.1.0 | 12.2.0 |
| DOMPurify | 3.4.16 | 3.4.17 |
| KaTeX | 0.16.47 | 0.18.10 |
| KaTeX's Commander dependency | 8.3.0 | 15.1.0 |

Commander is a transitive dependency selected by KaTeX. Its Node requirement is
`>=22.12.0`, within the project's documented Node.js 24+ requirement. No override
or forced audit fix was used. Mermaid 12.3.0 was available but was not needed.

The final audit reported zero vulnerabilities. This result covers the npm
advisory database at review time; it is not a full security assessment.

## Verification

- `npm test`: all 11 search tests passed.
- `.venv-embed/bin/python scripts/publish.py`: site and bundled assets built.
- `npm audit --json`: zero vulnerabilities after the updates.
- `git diff --check`: passed.
- `npm ci`: clean install from the updated lock file passed.
- `npm run test:browser`: all five Chromium tests passed.

npm also warned that esbuild's install script has no explicit `allowScripts`
approval. This is an npm configuration warning, not an audit finding. The asset
build succeeded with the installed esbuild binary.

## Advisory sources

- DOMPurify: [GHSA-cg2g-xh64-v4q7](https://github.com/advisories/GHSA-cg2g-xh64-v4q7),
  [GHSA-mrv2-3pqr-j5jr](https://github.com/advisories/GHSA-mrv2-3pqr-j5jr),
  [GHSA-c6gr-qvv4-5v3f](https://github.com/advisories/GHSA-c6gr-qvv4-5v3f).
- KaTeX: [GHSA-238p-pmpm-9mq7](https://github.com/advisories/GHSA-238p-pmpm-9mq7).

These identifiers and affected ranges came from the npm audit response.
