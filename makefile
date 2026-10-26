MLX_REPO = .mlx_CLXV_tmp
MLX_URL = https://github.com/42school/mlx_CLXV.git
VENV = .venv
PYTHON = $(CURDIR)/$(VENV)/bin/python
PIP = $(PYTHON) -m pip

.PHONY: all install mlx_install clean run debug lint lint-strict

all: install

mlx_install: install

install:
	@set -eu; \
	trap 'rm -rf "$(MLX_REPO)"' EXIT; \
	python3 -m venv "$(CURDIR)/$(VENV)"; \
	echo ".venv créé !"; \
	git clone --quiet "$(MLX_URL)" "$(MLX_REPO)"; \
	cd "$(MLX_REPO)"; \
	sh configure.sh > /dev/null; \
	$(MAKE) > /dev/null; \
	$(PIP) install -q mlx-*-py3-none-any.whl > /dev/null; \
	$(PIP) install -q numpy > /dev/null; \
	$(PIP) install -q flake8 > /dev/null; \
	echo; \
	printf "\033[32mDépendances installées avec succès.\033[0m\n"

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint:
	$(PYTHON) -m flake8 . --exclude=.venv,.mlx_CLXV_tmp
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores 
		--ignore-missing-imports --disallow-untyped-defs 
		--check-untyped-defs --exclude "(^|/)(\.venv|\.mlx_CLXV_tmp)/"

lint-strict:
	$(PYTHON) -m flake8 . --exclude=.venv,.mlx_CLXV_tmp
	$(PYTHON) -m mypy . --strict --exclude "(^|/)(\.venv|\.mlx_CLXV_tmp)/"

clean:
	rm -rf "$(MLX_REPO)"
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf maze.txt
	rm -rf "$(VENV)"
	rm -rf *.egg-info
	rm -rf dist/
