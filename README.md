*This activity has been created as part of the 42 curriculum by ytrabels and lherpet.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator with a graphical viewer. From a plain-text configuration file, the program:

1. generates a random maze (reproducible with a seed), either **perfect** (exactly one path between any two cells) or **non-perfect** (with loops);
2. reserves a block of fully closed cells drawing a visible **"42"** in the middle of the maze (when the maze is large enough);
3. computes the shortest path between the entry and the exit;
4. displays the maze with **MiniLibX (MLX)**;
5. writes the walls, the entry, the exit and the shortest path to an output file, using the hexadecimal format required by the subject.

The generation logic lives in a single reusable class, `MazeGenerator`, packaged as the `mazegen` module (see [Reusable module](#reusable-module)).

### Repository layout

```text
.
├── a_maze_ing.py                    # main program: config parsing + launch
├── config.txt                       # default configuration
├── makefile                         # install / run / debug / lint / clean
├── mazegen/
│   ├── __init__.py                  # exposes MazeGenerator
│   ├── class_maze.py                # MazeGenerator (generation, solver, output)
│   ├── mlx_draw.py                  # low-level MLX drawing helpers
│   └── mlx_run.py                   # MLX window, key hooks, colors
├── mazegen-1.0.0-py3-none-any.whl   # pip-installable package
├── pyproject.toml                   # build metadata for the package
├── LICENSE.md
└── README.md
```

## Instructions

### Requirements

- Python 3.10 or later
- NumPy
- The 42 MiniLibX Python bindings (`mlx`), from [mlx_CLXV](https://github.com/42school/mlx_CLXV)
- A graphical environment able to open an MLX window
- `flake8` and `mypy` for the lint rules

### Installation

```sh
make install
```

This creates a virtual environment in `.venv`, clones and builds MiniLibX, then installs the `mlx` wheel, `numpy`, `flake8` and `mypy` inside it.

### Run

```sh
make run
# equivalent to:
python3 a_maze_ing.py config.txt
```

The program takes exactly one argument: the configuration file. It opens the MLX window and writes the generated maze to the file named by `OUTPUT_FILE`.

### Other Makefile rules

| Rule | Description |
| --- | --- |
| `make debug` | Runs the program under `pdb`. |
| `make lint` | `flake8` + `mypy` with `--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`. |
| `make lint-strict` | `flake8` + `mypy --strict`. |
| `make clean` | Removes `__pycache__`, `.mypy_cache`, `.venv`, build artifacts and the generated `maze.txt`. |

### Graphical controls

| Key | Action |
| --- | --- |
| `0` | Close the window and quit. |
| `1` | Generate and display a new maze. |
| `2` | Show / hide the shortest path from entry to exit. |
| `3` | Change the wall color (picked at random in a palette of named colors). |

The cells of the "42" pattern are drawn in a distinct color (crimson).

### Error handling

The program reports a clear message instead of crashing when:

- the number of arguments is wrong, the file does not exist or is not valid UTF-8;
- a line is not of the form `KEY=VALUE`, a key is empty or duplicated, or a mandatory key is missing;
- a value has the wrong type (non-integer size, malformed coordinates, boolean that is neither `True` nor `False`);
- the entry or exit is outside the maze, entry and exit are identical, or one of them is on the "42" pattern;
- the maze is too small to host the "42" pattern (the pattern is then omitted and a notice is printed).

## Configuration file

The file contains one `KEY=VALUE` pair per line. Lines starting with `#` and empty lines are ignored. Keys are case-insensitive; surrounding spaces are stripped.

| Key | Required | Description | Example |
| --- | --- | --- | --- |
| `WIDTH` | yes | Maze width in cells (2 to 100). | `WIDTH=15` |
| `HEIGHT` | yes | Maze height in cells (2 to 100). | `HEIGHT=15` |
| `ENTRY` | yes | Entry cell, `x,y` (column, row), counted from 0. | `ENTRY=0,0` |
| `EXIT` | yes | Exit cell, `x,y`. Must differ from `ENTRY`. | `EXIT=14,14` |
| `OUTPUT_FILE` | yes | Path of the output file. | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True`: no loops. `False`: loops are added. | `PERFECT=True` |
| `SEED` | no | Integer seed for reproducible mazes. | `SEED=42` |
| `SHOW_FORTY_TWO` | no | `True` / `False`: draw the "42" pattern (default: `True`). | `SHOW_FORTY_TWO=True` |

Default `config.txt`:

```text
# Maze width
WIDTH=15
# Maze height
HEIGHT=15
# Entry coordinates
ENTRY=0,0
# Exit coordinates
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
# Show the 42 pattern
SHOW_FORTY_TWO=True
```

`x` is the horizontal position (column, from `0` to `WIDTH - 1`) and `y` the vertical position (row, from `0` to `HEIGHT - 1`). The "42" pattern is a 7 × 5 block centered in the maze; it needs a maze of at least **9 × 7** cells. Entry and exit cannot be placed on it.

## Output file

```text
9515391539551795151151153      <- one row of the maze per line
EBABAE812853C1412BA812812         (one hexadecimal digit per cell)
...
                               <- empty line
0,0                            <- entry (x,y)
14,14                          <- exit (x,y)
SSEESEEENNEE...                <- shortest path, letters N / E / S / W
```

Each cell is a hexadecimal digit whose bits tell which walls are **closed**:

| Bit | Direction |
| --- | --- |
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

Example: `A` (`1010`) means the East and West walls are closed. Walls shared by two neighbouring cells are always encoded consistently on both sides, and the outer border of the maze is always closed. All lines end with `\n`.

## Algorithm

### Generation: randomized Kruskal

Every cell starts closed (`0xF`) with its own region identifier. Then, repeatedly:

1. pick a random cell that still has a neighbour belonging to a different region (cells of the "42" pattern are excluded);
2. pick one such neighbour at random;
3. open the wall between the two cells and merge the two regions under a single identifier.

The loop stops when all cells outside the "42" pattern belong to one region. Since a wall is only opened between two *different* regions, no cycle can appear: the result is a spanning tree, i.e. a **perfect maze**.

When `PERFECT=False`, a second pass visits every cell outside the pattern; each cell that still has more than two closed walls opens one extra wall towards a random neighbour (not part of the "42" pattern). These additional openings create loops and reduce dead ends.

### Solving: wave propagation (BFS)

The solver labels cells with their distance from the entry, expanding step by step until the exit is reached. The path is then rebuilt by walking back from the exit, each time moving to a neighbour whose step is one lower. Because exploration is level by level, the path found is a **shortest path**.

### Why this algorithm

- Randomized Kruskal only needs local operations (a cell and one neighbour), which keeps the wall-removal logic simple.
- It never creates loops by construction, which gives the `PERFECT=True` guarantee for free.
- It extends naturally to non-perfect mazes by removing a few more walls afterwards.
- Seeding Python's `random` module makes every maze reproducible.

## Reusable module

The generation is implemented as one class, `MazeGenerator`, in the standalone `mazegen` package. A pre-built wheel, `mazegen-1.0.0-py3-none-any.whl`, is at the root of the repository.

### Install

```sh
pip install mazegen-1.0.0-py3-none-any.whl
```

Note: `mazegen` imports the MLX bindings, so `mlx` must be installed in the same environment (see [Installation](#installation)). NumPy is installed automatically.

### Rebuild the package from sources

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install build
python3 -m build          # produces dist/mazegen-1.0.0-py3-none-any.whl and .tar.gz
```

### Parameters

```python
MazeGenerator(
    width: int,
    height: int,
    seed=None,                       # int for reproducible mazes
    perfect: bool = True,            # False -> loops
    entry: tuple[int, int] = (0, 0), # (x, y)
    exit: tuple[int, int] | None = None,  # (x, y), default (width-1, height-1)
    show_forty_two: bool = True,
)
```

If a parameter is invalid (size below 2, entry/exit out of bounds or identical), an error is printed and `is_instanciable` is set to `False`; nothing is generated.

### Basic example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    seed=42,
    perfect=True,
    entry=(0, 0),
    exit=(19, 14),
    show_forty_two=True,
)

maze._generate()                 # generate without opening a window
maze.write_output("maze.txt")    # walls + entry + exit + shortest path

path = maze._get_path()[::-1]    # cells ordered from entry to exit
print([(c.y, c.x) for c in path])  # (x, y) coordinates
```

To generate **and** open the MLX viewer, call `maze.run()` instead of `maze._generate()`.

### Accessing the structure and a solution

| Attribute / method | Description |
| --- | --- |
| `maze.cells` | NumPy array `(height, width)` of `Cell` objects. For a cell, `cell.x` is the **row** and `cell.y` the **column**. |
| `maze.layer_wall` | NumPy array `(height, width)` of wall bitmasks (same bit meaning as the output file). |
| `maze.layer_id` | Region identifiers (all equal outside the "42" pattern once generated). |
| `cell.is_fourty_two` | `True` for cells of the "42" pattern. |
| `cell.step` | Distance from the entry (`-1` if not reached). |
| `maze._get_path()` | Shortest path as a list of cells, **from exit to entry**. |
| `maze.write_output(path)` | Writes the maze in the output file format. |
| `maze.run()` | Generates the maze and starts the MLX window. |

`MazeGenerator.Hex` provides the wall constants `NORTH = 1`, `EAST = 2`, `SOUTH = 4`, `WEST = 8`.

## Team and project management

### Roles

Individual project, carried out by `ytrabels` and `lherpet`: design, implementation, testing and integration.

### Planning and its evolution

The project was organized around a few main milestones:

1. Implement the maze data model and represent each cell's four walls with a hexadecimal bitmask.
2. Build the generation process, including the optional closed-cell pattern forming the 42 logo.
3. Find a shortest path between the entry and exit and serialize the maze in the required output format.
4. Add the MiniLibX viewer and controls for regenerating the maze, toggling the path, and changing the wall color.
5. Package the generator as the reusable `mazegen` module and document installation, configuration, and usage.

The work evolved from implementing the generator itself to integrating the solver, graphical interface, configuration parser, and distributable package. One of the harder parts was keeping the different representations consistent: coordinates are supplied as `(x, y)`, while the NumPy grid is indexed by row and column; wall openings also need to update both adjacent cells. Integrating the MLX viewer and making the package usable separately from the command-line entry point required additional attention.

### What worked well / what could be improved

Separating the maze logic into the `MazeGenerator` class and exposing it through the `mazegen` package makes the generator reusable outside the main script. The configuration file keeps common options accessible without editing the code, while the seed supports reproducible generation. The graphical controls also make it possible to inspect a maze and its shortest path interactively.

The project could be improved by adding automated tests for configuration errors, wall-bit consistency, path validity, reproducibility, and both perfect and non-perfect mazes. The public API could also be made clearer by documenting which methods are intended for external use and which methods are internal implementation details. More systematic validation of constructor arguments and clearer separation between generation, solving, and rendering would make future maintenance easier.

### Tools

Python, NumPy, MiniLibX, Make, flake8, mypy, Git.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [NumPy documentation](https://numpy.org/doc/)
- [MiniLibX for 42 (mlx_CLXV)](https://github.com/42school/mlx_CLXV)
- [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python Packaging User Guide](https://packaging.python.org/)
- 42 *A-Maze-ing* subject, version 1.4

### Use of AI

AI was used as an assistant, not as a code generator for the core logic:

- reviewing the entry/exit coordinate conventions (`x,y` in the config and output file vs. row/column in the code);
- drafting and checking this README against the subject requirements.

All AI output was reviewed, tested and is understood by the author.

## License

See [LICENSE.md](LICENSE.md).
