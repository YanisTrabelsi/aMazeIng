import mazegen as mg
import sys


class MazeGenerationError(Exception):
    """Exception if the maze can not be generated because of config.txt file"""

    def __init__(self, message):
        self.message = message


def redprint(s: str):
    print(f"\033[31m{s}\033[0m")


def config_parser(file: str) -> dict:
    config_dict: dict[str, str] = {}
    with open(sys.argv[2], "r") as config:
        for line in config:
            striped_line = line.strip()
            if len(striped_line) == 0:
                continue
            if striped_line.startswith("#"):
                continue
            text: list[str] = striped_line.split("=")
            if len(text) != 2:
                raise MazeGenerationError(
                    "\033[31mWrong syntaxe, should be 'PERFECT=True' for exemple\033[0m"
                )
            config_dict[text[0].strip()] = text[1].strip()
    return config_dict


def dict_parser(config_dict: dict[str, str]) -> bool:

    can_run: bool = True

    try:
        width: int = int(config_dict["WIDTH"])
        if width < 2 or width > 100:
            raise MazeGenerationError(
                "\033[31mWIDTH have to be between 2 and 100\n\033[0m"
            )

            can_run = False
    except MazeGenerationError as e:
        redprint(f"Error: {e}")

    return can_run


if __name__ == "__main__":
    if len(sys.argv) != 3:
        redprint("Usage <python3 a_maze_ing.py config.txt>")
        sys.exit(1)
    if sys.argv[2] != "config.txt":
        redprint("Usage <python3 a_maze_ing.py config.txt>")
        sys.exit(1)

    config_dict: dict[str, str] | None = None
    try:
        config_dict = config_parser(sys.argv[2])
    except MazeGenerationError as e:
        redprint(f"Error: {e}")
    if config_dict is not None:
        dict_parser(config_dict)

        params = {
            "width": int(config_dict["WIDTH"]),
            "height": int(config_dict["HEIGHT"]),
            "seed": int(config_dict["SEED"]),
            "perfect": config_dict["PERFECT"],
            "entry": config_dict["ENTRY"],
            "exit": config_dict["EXIT"],
        }
        MazeGenerator: mg.MazeGenerator = mg.MazeGenerator(**params)
        MazeGenerator.sync_valid
