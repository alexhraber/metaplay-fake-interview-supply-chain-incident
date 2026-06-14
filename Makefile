.PHONY: sync kernels notebooks sanitize render check jupyter clean-rendered

sync:
	uv sync

kernels:
	jupyter kernelspec list

notebooks:
	python scripts/build-public-notebooks.py

sanitize:
	python scripts/sanitize-notebooks.py --write notebooks

render: sanitize
	bash scripts/render-notebooks.sh

check:
	bash scripts/check-public-safety.sh

jupyter:
	jupyter lab

clean-rendered:
	rm -f docs/notebooks/*.html

