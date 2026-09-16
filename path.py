import json
import numpy.typing as npt


with open("data.json") as f:
    data = json.load(f)

ENTRY = data["ENTRY"]
EXIT = data["EXIT"]


def find(cells: npt.NDArray):
    ...
