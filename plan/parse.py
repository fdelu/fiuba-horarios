import re
import json
import os

# Regex
CODIGO = r"^(\d\d\.\d\d)"
NOMBRE = r" (([^\W\d_]|\s)*) (\d|\()"
CREDITOS = r"([^\W\d_]|\s)* (?:\(\*+\) )?(\d+)"
CORRELATIVAS = r"(\d\d\.\d\d)"
MIN_CREDITOS = r"(\d+) créditos aprobados"

DIR = os.path.dirname(os.path.realpath(__file__))
RAW_DATA = f"{DIR}/raw.txt"
OUTPUT = f"{DIR}/data.json"


def parse_raw(creditos):
    with open(RAW_DATA, "r", encoding="utf8") as f:
        lines = list(f.readlines())

    arr = []
    for line in lines:
        codigo = re.search(CODIGO, line)[0].replace(".", "")
        name = re.search(NOMBRE, line)[1]
        print(name)
        credits = int(re.search(CREDITOS, line).groups()[-1])
        dependencies = re.findall(CORRELATIVAS, line)
        dependencies = [x.replace(".", "") for x in dependencies]
        dependencies.remove(codigo)
        min_credits = re.search(MIN_CREDITOS, line)
        min_credits = int(min_credits[1]) if min_credits else 0

        arr.append({
            "codigo": codigo,
            "nombre": name,
            "creditos": credits,
            "correlativas": dependencies,
            "min_creditos": min_credits
        })

    with open(OUTPUT, "w", encoding="utf8") as f:
        json.dump({
            "creditos": creditos,
            "materias": arr
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parse_raw(286)
