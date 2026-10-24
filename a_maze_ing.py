import mazegen as mg
from mlx_run import Mlx_handler
import sys
from typing import Any


class ConfigError(Exception):
    pass


def redprint(s: str) -> str:
    return f"\033[31m{s}\033[0m"


def config_parser(file: str) -> dict:
    config_dict: dict[str, str] = {}
    try:
        with open(file, "r", encoding="utf-8") as config:
            for line_number, line in enumerate(config, start=1):
                striped_line = line.strip()
                if striped_line.startswith("#") or striped_line == "":
                    continue
                text: list[str] = striped_line.split("=", maxsplit=1)
                if len(text) != 2:
                    raise ConfigError(
                        f"wrong format at line {line_number}. Should be 'KEY=VALUE"
                    )
                key = text[0].strip()
                if key == "":
                    raise ConfigError(f"missing key at line {line_number}")
                if key in config_dict:
                    raise ConfigError(f"duplicate key at line {line_number}")
                config_dict[key] = text[1].strip()
    except OSError as error:
        raise ConfigError(f"Cannot read '{file}': {error}")
    except UnicodeDecodeError:
        raise ConfigError(f"error while reading the file: Should be a UTF-8 text file")
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


def parse_entry_exit(
    config_dict: dict[str, str], key: str, width: int, height: int
) -> tuple[int, int]:

    coordinate = config_dict[key].split(",")

    if len(coordinate) != 2:
        raise ConfigError(f"{key} should look like 'x,y', got '{config_dict[key]}'")

    try:
        x, y = int(coordinate[0]), int(coordinate[1])
    except ValueError:
        raise ConfigError(
            f"{key} has to contain two integers, got '{config_dict[key]}'"
        )

    if x < 0 or x >= width:
        raise ConfigError(f"{key}=(x,y): x has to be between 0 and {width - 1}")

    if y < 0 or y >= height:
        raise ConfigError(f"{key}=(x,y): y has to be between 0 and {height - 1}")

    return (y, x)


def dict_parser(config_dict: dict[str, str]) -> dict[str, Any]:

    mandatory_list: list[str] = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    missing_key = [key for key in mandatory_list if key not in config_dict]
    if missing_key:
        raise ConfigError(f"missing key(s): {', '.join(missing_key)}")

    width = parse_int(config_dict, "WIDTH")
    height = parse_int(config_dict, "HEIGHT")
    entry = parse_entry_exit(config_dict, "ENTRY", width, height)
    exit_cell = parse_entry_exit(config_dict, "EXIT", width, height)

    if exit_cell == entry:
        raise ConfigError("ENTRY and EXIT can't be at the same place")

    if config_dict["PERFECT"] not in ("True", "False"):
        raise ConfigError(
            f"PERFECT has to be True or False, got '{config_dict['PERFECT']}'"
        )

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
        print(redprint("Usage <python3 a_maze_ing.py config.txt>"))
        sys.exit(1)

    try:
        config: dict[str, Any] = dict_parser(config_parser(sys.argv[1]))
        generator = mg.MazeGenerator(
            config["width"],
            config["height"],
            config["seed"],
            config["perfect"],
            config["entry"],
            config["exit"],
        )
        generator.matrix_init()
        generator.init_layers()
        generator.init_cells()
        generator.run()
        generator.write_output(config["output_file"])
        mlx_hander = Mlx_handler(config["width"], config["height"], generator.cells)
    except ConfigError as e:
        print(f"{redprint('[Error]')} {e}")
        sys.exit(1)
    except OSError as e:
        print(f"{redprint('[Error]')} {e}")
