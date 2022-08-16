import json
import requests
import re

L = "A-Za-zÁÉÍÓÚÚáéíóúÑñüÜ"

with open("input.txt", "r", encoding="utf8") as f:
    passed = set(map(lambda x: int(x.replace(".", "").strip()), f.readlines()))

with open("data.json", "r", encoding="utf8") as f:
    data = json.load(f)
    data = {x["number"]: x for x in data}

credits = 0
for subject in passed:
    credits += data[subject]["credits"]

has_language = any(map(lambda x: "idioma" in data[x]["name"].lower(), passed))

response = requests.get(
    "https://guaraniautogestion.fi.uba.ar/g3w/horarios_cursadas?formulario_filtro[ra]=3b5e0365f0c2299dfd89eb3852a8ebb566382194&formulario_filtro[carrera]=9220d714727dbe74790a6782a5241e56f7034064&formulario_filtro[anio_cursada]=&formulario_filtro[periodo]=29")
available = set(
    map(int, re.findall(rf"[\.{L}]+ \( (\d\d\d\d) \)", response.text)))

can_do = set()
for number, info in data.items():
    if not all(map(lambda x: x in passed, info["dependencies"])) \
            or info["min_credits"] > credits \
            or number in passed \
            or (has_language and "idioma" in info["name"].lower()):
        continue
    can_do.add(number)


def print_subject(subject):
    print(
        f'* {subject["name"]} ({subject["number"]}) - {subject["credits"]} créditos')


print("Calculadora de materias")
print(f"Aprobaste {len(passed)} materias")
print(f"Tenés {credits}/248 ({credits / 248 * 100 :.2f}%) créditos de la carrera aprobados (no cuenta CBC)\n")
if has_language:
    print("Ya cursaste una materia electiva de idioma, asi que no podes cursar otra\n")
print("Podes cursar las siguientes materias: ")
for number in sorted(can_do.intersection(available), key=lambda x: data[x]["name"]):
    print_subject(data[number])
print("\nTambién podrías cursar las siguientes materias, pero no tienen horarios este cuatrimestre:")
for number in sorted(can_do.difference(available), key=lambda x: data[x]["name"]):
    print_subject(data[number])
