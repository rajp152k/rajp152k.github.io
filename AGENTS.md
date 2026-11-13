# Authoring work

Treat a request to prepare a post as the complete writing workflow. Read
[docs/writing.md](docs/writing.md) and [docs/editorial-policy.md](docs/editorial-policy.md).
Run `./prepare.sh status` first. Read each changed draft in full. Complete the
reader and references reviews, maintain terms.json, update only affected review
records, and run `./prepare.sh build`. Report the preview and open questions.
Do not ask raj to name each stage.

Meditations are raj's prose. Ask before editing them. Write logs only when
requested. Maintain supporting records yourself when sources and meaning are
clear. Ask about uncertain meaning outside article prose. Record actual reviews,
not a blanket completion statement. Review all affected posts after a shared change.

Use `.preparation.json` for current reviews, decisions, reading choices, and
questions. It is committed internal state, excluded from the public site. The
archive review document records the initial review; records track later work.

For release, run `sh scripts/verify_preparation.sh`. Commit only intended files
when checks pass. Keep model calls out of builds and CI. Separate publication
approval from preparation. Push, merge, deploy, or run publish.sh only with
explicit authority. After authorized publication, check deployment and the live
page before reporting success.
