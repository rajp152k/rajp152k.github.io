prepare:
	./prepare.sh build

preview:
	./prepare.sh preview

status:
	./prepare.sh status

check:
	sh scripts/verify_preparation.sh

# Low-level commands for focused work.
embed:
	sh scripts/python.sh scripts/embed.py

build:
	sh scripts/python.sh scripts/publish.py

# Compatibility alias for the former embed/build/serve sequence.
e2e: preview
