embed:
	.venv-embed/bin/python scripts/embed.py

check:
	.venv-embed/bin/python scripts/embed.py --check

build: 
	.venv-embed/bin/python scripts/publish.py

e2e:
	just embed
	just build
	.venv-embed/bin/python -m http.server 8765 --directory site
