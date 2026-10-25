MLX_REPO = .mlx_CLXV_tmp
MLX_URL = https://github.com/42school/mlx_CLXV.git

.PHONY: all mlx_install clean run debug lint lint-strict

all: mlx_install
	@echo "MLX installée."

install:
	@set -eu; \
	trap 'rm -rf "$(MLX_REPO)"' EXIT; \
	python3 -m venv .venv;
	source .venv/bin/activate;
	git clone "$(MLX_URL)" "$(MLX_REPO)"; \
	cd "$(MLX_REPO)"; \
	sh configure.sh; \
	$(MAKE); \
	python3 -m pip install mlx-*-py3-none-any.whl;
	python3 -m pip install numpy;
	rm -rf "$(MLX_REPO)"

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm -rf $(MLX_REPO)
	rm -rf __pycache__
	rm -rf maze.txt
	rm -rf .venv

