import json


def parser_tojson() -> None:
    with open("./config.txt", "r") as f:
        data: list[list[str]] = []
        for line in f:
            if len(line) > 3:
                data.append(line.translate(str.maketrans("", "", "#\n\32")).split("="))
    with open("./data.json", "w") as f:
        f.write(json.dumps(dict(data), indent=4))
