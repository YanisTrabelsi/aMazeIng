import mazegen as mg
import sys
from typing import Any


class ConfigError(Exception):
    """Exception if the maze can not be generated because of config.txt file"""

    def __init__(self, message):
        self.message = message


def redprint(s: str):
    print(f"\033[31m{s}\033[0m")


def config_parser(file: str) -> dict:
    config_dict: dict[str, str] = {}
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as config:
            for line_number, line in enumerate(config, start=1):
                striped_line = line.strip()
                if striped_line.startswith("#") or striped_line == "":
                    continue
                text: list[str] = striped_line.split("=", maxsplit=1)
                if len(text) != 2:
                    raise ConfigError(f"{redprint('[Error]')} wrong format at line {line_number}. Should be 'KEY=VALUE")
                key = text[0].strip()
                if key == "":
                    raise ConfigError(f"{redprint('[Error]')} missing key at line {line_number}")
                if key in config_dict:
                    raise ConfigError(f"[Error] duplicate key at line {line_number}")
                config_dict[key] = text[1].strip()
    except OSError as error:
        raise ConfigError(f"{redprint('[Error]')} Cannot read '{file}': {error}")
    except UnicodeDecodeError as error:
        raise ConfigError(f"{redprint('[Error]')} error while reading the file: Should be a UTF-8 text file")
    return config_dict


def parse_int(config_dict: dict[str, str], key: str) -> int:

    try:
        value = int(config_dict[key])
    except ValueError:
        raise ConfigError(f"{key} has to be an integer, got '{config_dict[key]}'")
    if key in ("WIDTH", "HEIGHT"):
        if value < 2 or value > 100:
            raise ConfigError(f"{key} has to be between 2 and 100")
    return value


def parse_entry_exit(config_dict: dict[str, str], key: str, width: int, height: int) -> tuple[int, int]:

    coordinate = config_dict[key].split(",")

    if len(coordinate) != 2:
        raise ConfigError(f"{key} should look like 'x,y', got '{config_dict[key]}'")

    try:
        x, y = int(coordinate[0]), int(coordinate[1])
    except ValueError:
        raise ConfigError(f"{key} has to contain two integers, got '{config_dict[key]}'")

    if x < 0 or x >= width:
        raise ConfigError(f"{key}=(x,y): x has to be between 0 and {width - 1}")

    if y < 0 or y >= height:
        raise ConfigError(f"{key}=(x,y): y has to be between 0 and {height - 1}")

    return (x, y)


def dict_parser(config_dict: dict[str, str]) -> dict[str, Any]:

    mandatory_list: list[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    missing_key = [key for key in mandatory_list if key not in config_dict]
    if missing_key:
        raise ConfigError(f"missing key(s): {', '.join(missing)}")

    width = parse_int(config_dict, "WIDTH")
    height = parse_int(config_dict, "HEIGHT")
    entry = parse_entry_exit(config_dict, "ENTRY", width, height)
    exit_cell = parse_entry_exit(config_dict, "EXIT", width, height)

    if exit_cell == entry:
        raise ConfigError("ENTRY and EXIT can't be at the same place")

    if config_dict["PERFECT"] not in ("True", "False"):
        raise ConfigError(f"PERFECT has to be True or False, got '{config_dict['PERFECT']}'")

    if config_dict["OUTPUT_FILE"] == "":
        raise ConfigError("OUTPUT_FILE can't be empty")

    seed = None
    if "SEED" in config_dict:
        seed = parse_int(config_dict, "SEED")

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_cell,
        "perfect": config_dict["PERFECT"] == "True",
        "seed": seed,
        "output_file": config_dict["OUTPUT_FILE"],
    }



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
