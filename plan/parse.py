import re
import json
L = "A-Za-zÁÉÍÓÚÚáéíóúÑñüÜ"
arr = []

with open("raw.txt", "r", encoding="utf8") as f:
    for line in f.readlines():
        number = int(re.search("^(\d\d\.\d\d)", line)[0].replace(".", ""))
        name = re.search(rf" ([\s{L}]*) (\d|\()", line)[1]
        print(name)
        credits = int(re.search(rf"[\s{L}]* (?:\(\*+\) )?(\d+)", line)[1])
        dependencies = re.findall(r"(\d\d\.\d\d)", line)
        dependencies = [int(x.replace(".", "")) for x in dependencies]
        dependencies.remove(number)
        min_credits = re.search(r"(\d+) créditos aprobados", line)
        min_credits = int(min_credits[1]) if min_credits else 0

        arr.append({
            "number": number,
            "name": name,
            "credits": credits,
            "dependencies": dependencies,
            "min_credits": min_credits
        })

with open("data.json", "w", encoding="utf8") as f:
    json.dump(arr, f, ensure_ascii=False, indent=2)
