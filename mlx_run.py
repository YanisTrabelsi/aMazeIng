from mlx import Mlx
import numpy.typing as npt
from .mlx_draw import put_path


class Mlx_handler:
    def __init__(self, width: int, height: int, cells: npt.NDArray) -> None:
        self.width: int = width
        self.height: int = height
        self.cell_size: int = 40
        self.wall_size: int = 2
        self.win_width: int = width * self.cell_size
        self.win_height: int = height * self.cell_size
        self.color: int = 0xFF40E0D0

        m = Mlx()
        mlx = m.mlx_init()
        win = m.mlx_new_window(mlx, self.win_width, self.win_height, "Test")

        for cell in cells.flat:
            put_path(mlx, win, cell.y, cell.y, self.color)
