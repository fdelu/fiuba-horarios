import re
import json
from bs4 import BeautifulSoup

# Regex a utilizar
# NOMBRE_MATERIA = "Actividad: (.*) \("
CODIGO_MATERIA = "\((\d\d\d\d)\)"
CODIGO_CURSO = "Comisión: (CURSO:? ?)?([\w-]+)"
CUPOS = r"(\d+) \/ \d+"
HORARIOS = "(\d\d:\d\d) a (\d\d:\d\d)"
PERIODO = "Período lectivo: (.*) "
DATA = r"kernel\.renderer\.on_arrival\((.*)\);"


def parse_html(html):
    data = json.loads(
        re.search(DATA, html)[1])
    parsed_html = BeautifulSoup(data.get("content"), "lxml")
    periodos = {}
    for periodo in parsed_html.find_all("div", attrs={"class": "js-recuadro_periodo"}):
        name = re.search(PERIODO, periodo.next_element.text)[1]
        periodos[name] = parse_periodo(periodo)
    return periodos


def parse_periodo(periodo):
    cursos = {}
    for materia in periodo.find_all("div", attrs={"class": "js-recuadro_actividad"}):
        codigo = parse_codigo_materia(materia)
        cursos_materia = []
        for curso in materia.find_all("table"):
            curso = parse_curso(curso)
            if curso:
                cursos_materia.append({"materia": codigo, **curso})
        cursos[codigo] = cursos_materia

    return cursos


def parse_codigo_materia(materia):
    header = materia.find("h4").text
    return re.search(CODIGO_MATERIA, header)[1]


def parse_curso(curso):
    docentes = curso["docentes"].split(", ")

    info = str(curso.find("tr", attrs={"class": "comision"}))
    if "condicionales" in info.lower():
        return

    codigo = re.search(CODIGO_CURSO, info, re.IGNORECASE).groups()[-1]
    cupos = re.search(CUPOS, info)
    cupos = int(cupos[1]) if cupos else None

    horarios = {}
    for entry in curso.find_all("tr", attrs={"class": "js-dia"}):
        dia = entry["dia_sem"].lower()
        horas = horarios.get(dia, [])
        inicio, fin = re.search(
            HORARIOS, entry.text).groups()
        horas.append({"inicio": inicio, "fin": fin})
        horarios[dia] = horas

    return {
        "codigo": codigo,
        "cupos": cupos,
        "horarios": merge_overlapped(horarios),
        "docentes": docentes
    }


def merge_overlapped(horarios):
    for dia in horarios:
        horas = sorted(horarios[dia], key=lambda x: x["inicio"])
        new_horas = []
        for i in range(len(horas)):
            if i == 0:
                new_horas.append(horas[i])
                continue
            if horas[i]["inicio"] <= horas[i - 1]["fin"]:
                new_horas[-1]["fin"] = horas[i]["fin"]
            else:
                new_horas.append(horas[i])
        horarios[dia] = new_horas
    return horarios
