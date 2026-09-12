import json


def parser_tojson() -> None:
    with open('./config.txt', 'r') as f:
        data: list[list[str]] = []
        for line in f:
             data.append(line.translate(str.maketrans("", "", "#\n")).split('='))
        for i, e in enumerate(data):
            if (len(e[0]) == 0):
                data.pop(i)

    with open('./data.json', 'w') as f:
        f.write(json.dumps(dict(data), indent=4))
parser_tojson()
