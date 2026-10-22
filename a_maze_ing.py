from mazegen import MazeGenerator
import sys


def config_parser(file: str) -> dict:
    config_dict: dict[str, str] = {}
    with open(sys.argv[1], "r", encoding="utf-8") as config:
        for line in config:
            striped_line = line.strip()
            if striped_line.startswith("#"):
                continue
            text = striped_line.split("=")
            if len(text) != 2:
                raise ValueError("Wrong syntaxe, should be 'PERFECT=True' for exemple")
            config_dict[text[0].strip()] = text[1].strip()
    return config_dict


def dict_parser(config_dict: dict[str, str]) -> bool:

    can_run: bool = True
    try:
        width: int = int(config_dict["WIDTH"])
        if width < 2 or width > 100:
            print("WIDTH have to be between 2 and 100\n")
            can_run = False
    except:
        print



if __name__ = "__main__":

    if len(sys.argv) != 2:
        print("Try: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config_dict: dict[str, str] = config_parser(sys.argv[1])
    except ValueError:
