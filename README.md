*This activity has been created as part of the 42 curriculum by ytrabels.*

# aMazeIng

## Description

aMazeIng is a Python maze generator and visualizer. It builds a grid maze, marks an entry and an exit, finds a route between them, displays the maze with MiniLibX, and writes the walls and route to an output file.

The generator supports two modes through `PERFECT`:

- `True`: keep the maze without loops.
- `False`: open additional walls to create loops.

The project also places a closed-cell pattern shaped like “42” in the center when the grid is large enough for it.

## Instructions

### Requirements

- Python 3.10 or later
- NumPy
- The Python MiniLibX package used by 42 (`mlx`)
- A graphical environment supported by MiniLibX

Install the Python dependencies in the environment you intend to use. The Makefile includes an `install` target for the 42 MiniLibX setup, as well as `run`, `debug`, `lint`, `lint-strict`, and `clean` targets.

### Run

The repository includes `config.txt` as a default configuration. From the repository root, run:

```sh
python3 a_maze_ing.py config.txt
```

Or use:

```sh
make run
```

The program takes one configuration file as its argument. It opens the graphical maze window and writes the generated maze to the file named by `OUTPUT_FILE`.

### Configuration file

The file contains one `KEY=VALUE` pair per line. Blank lines and lines beginning with `#` are ignored. The following keys are required:

| Key | Meaning | Example |
| --- | --- | --- |
| `WIDTH` | Maze width in cells, from 2 to 100. | `WIDTH=15` |
| `HEIGHT` | Maze height in cells, from 2 to 100. | `HEIGHT=15` |
| `ENTRY` | Entry coordinate in `x,y` order. | `ENTRY=6,13` |
| `EXIT` | Exit coordinate in `x,y` order. | `EXIT=14,1` |
| `OUTPUT_FILE` | Destination path for the generated maze. | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to keep the maze without loops. | `PERFECT=True` |

`ENTRY` and `EXIT` are distinct coordinates, counted from zero. The first number is horizontal position `x` (column), in the range `0` to `WIDTH - 1`. The second is vertical position `y` (row), in the range `0` to `HEIGHT - 1`.

The optional `SEED` key makes randomized generation reproducible:

```text
WIDTH=15
HEIGHT=15
ENTRY=6,13
EXIT=14,1
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Graphical controls

- `0`: close the window.
- `1`: generate another maze.
- `2`: show the route from entry to exit.
- `3`: hide the displayed route.

### Output file

The output contains one hexadecimal digit per cell, one row per line. Each digit encodes closed walls using bits 0–3 for North, East, South, and West respectively. After the grid, the file contains a blank line, the entry coordinate, the exit coordinate, and the route as `N`, `E`, `S`, and `W` letters.

## Algorithm

The maze starts with separate cell regions. The generator repeatedly chooses a cell and one of its eligible neighboring cells, opens the wall between them, and merges their region identifiers. It stops when all traversable cells belong to one connected region. This is a randomized Kruskal-style spanning-tree procedure: choosing edges at random and merging components builds a connected maze without loops. When `PERFECT=False`, the generator then opens additional eligible walls to add loops.

This algorithm was chosen because it creates a connected maze while keeping the wall-removal logic local to neighboring cells. Random selection, combined with the optional seed, gives varied but reproducible mazes.

## Reusable generator

The reusable maze-generation class is `MazeGenerator`, available from the `mazegen` module. It accepts the width, height, optional seed, `perfect` mode, entry, and exit. Coordinates passed to the class use `(x, y)` order.

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=15,
    height=15,
    seed=42,
    perfect=True,
    entry=(6, 13),
    exit=(14, 1),
)
maze.generate()

cells = maze.cells       # NumPy array containing the generated cells
solution = maze.get_path()  # Cells from exit back to entry
```

`maze.cells` provides access to the generated structure. `maze.get_path()` returns the solution as a list of cell objects, ordered from exit to entry. `maze.write_output(path)` writes the maze and solution in the project output format. The module can be imported from this repository with `from mazegen import MazeGenerator`. The repository does not currently contain build metadata or a wheel for pip installation.

## Team and project management

### Team roles

This repository's Git history identifies `ytrabels` as its author. The project is documented here as an individual activity; the author is responsible for implementation, testing, and integration.

### Planning and retrospective

The repository does not contain a project plan or retrospective, so the timeline and what worked well or could be improved must be completed by the author from their own project experience before submission. No schedule or retrospective details are inferred from code history.

### Tools

The repository uses Python, NumPy, MiniLibX, Make, Flake8, and Mypy. Git is used for version control. AI assistance was used to review the coordinate conventions in the entry/exit handling and to draft and check this README against the subject requirements. The generated text and code changes should be reviewed by the author.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [NumPy documentation](https://numpy.org/doc/)
- [MiniLibX for 42](https://github.com/42school/mlx_CLXV)
- [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- 42 *A-Maze-ing* subject, version 1.4 (`en.subject-34.pdf`)

