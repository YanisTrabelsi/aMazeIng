import mazegen as mg
import sys


class ConfigError(Exception):
    """Exception if the maze can not be generated because of config.txt file"""

    def __init__(self, message):
        self.message = message


def redprint(s: str):
    print(f"\033[31m{s}\033[0m")


def config_parser(file: str) -> dict:
    config_dict: dict[str, str] = {}
    try:
        with open(sys.argv[1], "r") as config:
            for line_number, line in enumerate(config, start=1):
                striped_line = line.strip()
                if striped_line.startswith("#") or striped_line == "":
                    continue
                text: list[str] = striped_line.split("=", maxsplit=1)
                if len(text) != 2:
                    raise ConfigError(f"[Error] wrong format at line {line_number}. Should be 'KEY=VALUE")
                key = text[0].strip()
                if key == "":
                    raise ConfigError(f"[Error] missing key at line {line_number}")
                if key in config_dict:
                    raise ConfigError(f"[Error] duplicate key at line {line_number}")
                config_dict[key] = text[1].strip()
    except (FileNotFoundError, IsADirectoryError):
        redprint("[Error] Wrong config file input")
    print(config_dict)
    return config_dict


def dict_parser(config_dict: dict[str, str]) -> bool:

    can_run: bool = True
    mandatory_config: list[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    try:

        for key in mandatory_config:
            if key not in config_dict:
                print(f"{redprint("[Error]")} {key} is missing in the config file")
                can_run = False
        if not can_run:
            return can_run

        width: int = int(config_dict["WIDTH"])
        if width < 2 or width > 100:
            raise ConfigError("WIDTH have to be between 2 and 100")

        height: int = int(config_dict["HEIGHT"])
        if height < 2 or height > 100:
            raise ConfigError("HEIGHT have to be between 2 and 100")

        x, y = config_dict["ENTRY"].split(",")
        entry: tuple[int, int] = (int(y), int(x))
        if x < 0 or x >= width:
            raise ConfigError(f"ENTRY=(x,y): x have to be between 0 and {width - 1}")
        if y < 0 or y >= height:
            raise ConfigError(f"ENTRY=(x,y): y have to be between 0 and {height - 1}")

        x, y = config_dict["EXIT"].split(",")
        exit: tuple[int, int] = (int(y), int(x))
        if x < 0 or x >= width:
            raise ConfigError(f"EXIT=(x,y): x have to be between 0 and {width - 1}")
        if y < 0 or y >= height:
            raise ConfigError(f"EXIT=(x,y): y have to be between 0 and {height - 1}")
        if exit == entry:
            raise ConfigError("Entry and Exit can't be at the same place")

    except ConfigError as e:
        redprint(f"Error: {e}")
        can_run = False
    return can_run


if __name__ == "__main__":

    if len(sys.argv) != 2:
        redprint("Usage <python3 a_maze_ing.py config.txt>")
        sys.exit(1)

    config_dict: dict[str, str] | None = None
    try:
        config_dict = config_parser(sys.argv[1])
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
