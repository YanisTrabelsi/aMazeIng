from mlx import Mlx
import draw as d
import numpy as np

BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
RED   = 0xFFFF0000
GREEN = 0xFF00FF00
BLUE  = 0xFF0000FF

def key_event(keycode, param):
    if keycode == 113:
        m.mlx_loop_exit(mlx)

m = Mlx()
mlx = m.mlx_init()
win = m.mlx_new_window(mlx, 600, 600, "Test")

grid = np.arange((600//30) * (600//30)).reshape(600//30, 600//30)
print(grid)

d.put_cell(mlx, win, 10, 10, RED, "f")
m.mlx_key_hook(win, key_event, None)
m.mlx_loop(mlx)

