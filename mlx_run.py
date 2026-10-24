from mlx import Mlx
import numpy.typing as npt
from mlx_draw import put_cell


class Mlx_handler:
    def __init__(self, width: int, height: int, cells: npt.NDArray) -> None:
        self.width: int = width
        self.height: int = height
        self.cell_size: int = 40
        self.wall_size: int = 2
        self.win_width: int = width * self.cell_size + 50
        self.win_height: int = height * self.cell_size + 50
        self.color: int = 0xFF40E0D0
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.mlx, self.win_width, self.win_height, "Test"
        )

        def key_hook(keycode, param) -> None:
            if keycode == 113:
                self.m.mlx_loop_exit(self.mlx)

        def loop(params):
            for cell in cells.flat:
                put_cell(
                    self.mlx,
                    self.win,
                    cell.y * self.cell_size + 25,
                    cell.x * self.cell_size + 25,
                    self.color,
                    cell.get_wall,
                )

        self.m.mlx_key_hook(self.win, key_hook, self)
        self.m.mlx_loop_hook(self.mlx, loop, None)
        self.m.mlx_loop(self.mlx)
