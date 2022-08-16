import json
from itertools import starmap
from calculadora import get_creditos, get_combinaciones_posibles, get_materias_disponibles, get_materias_posibles, es_idioma
import os

DIR = os.path.dirname(os.path.realpath(__file__))
PATH_PLAN = DIR + "/plan/data.json"
PATH_APROBADAS = DIR + "/aprobadas.txt"
PATH_OUTPUT = DIR + "/output.txt"
CREDITOS_PLAN = 248

with open(PATH_PLAN, "r", encoding="utf8") as f:
    PLAN = json.load(f)
    PLAN = {x["codigo"]: x for x in PLAN}


def format_materia(materia):
    materia = PLAN[materia]
    return f'* {materia["nombre"]} ({materia["codigo"]}) - {materia["creditos"]} créditos'


def format_dia(dia, horarios):
    return f"{dia.capitalize()}: {', '.join(map(lambda x: x['inicio'] + ' - ' + x['fin'], horarios))}."


def format_curso(curso):
    out = f"\tCurso {curso['codigo']}, {curso['cupos']} cupos\n"
    out += f"\t" + " ".join(starmap(format_dia, curso['horarios'].items()))
    out += f"\n\tDocentes: " + ', '.join(curso['docentes']) + "\n"
    return out


def resumen_disponibles():
    with open(PATH_APROBADAS, "r", encoding="utf8") as f:
        aprobadas = set(map(lambda x: x.replace(
            ".", "").strip(), f.readlines()))

    creditos = get_creditos(aprobadas)
    posibles = set(get_materias_posibles(aprobadas))
    disponibles = set(get_materias_disponibles())

    print(f"Aprobaste {len(aprobadas)} materias")
    print((f"Tenés {creditos}/{CREDITOS_PLAN} ({creditos / CREDITOS_PLAN * 100 :.2f}%) "
           "créditos de la carrera aprobados (no cuenta CBC)\n"))

    if any(es_idioma(materia) for materia in aprobadas):
        print("Ya cursaste una materia electiva de idioma, asi que no podes cursar otra\n")

    print("Podes cursar las siguientes materias: ")
    for codigo in sorted(posibles.intersection(disponibles), key=lambda x: PLAN[x]["nombre"]):
        print(format_materia(codigo))

    print("\nTambién podrías cursar las siguientes materias, pero no tienen horarios este cuatrimestre:")
    for codigo in sorted(posibles.difference(disponibles), key=lambda x: PLAN[x]["nombre"]):
        print(format_materia(codigo))

    return posibles.intersection(disponibles)


def input_materias(mensaje):
    materias = input(f"{mensaje} (códigos separados por comas) ").split(",")
    return list(map(lambda x: x.strip(), filter(len, materias)))


def guardar_output(combinaciones):
    print(f"Escribiendo resultado a {PATH_OUTPUT}")
    with open(PATH_OUTPUT, "w", encoding="utf8") as f:
        for i, combinacion in enumerate(combinaciones):
            f.write(f"Opción {i+1}\n")
            for materia, curso in combinacion:
                f.write(format_materia(materia) + "\n")
                f.write(format_curso(curso))
            f.write("\n")


def main():
    print("Calculadora de materias")
    materias = resumen_disponibles()
    cantidad = int(input("\n¿Cuántas materias queres cursar? "))
    excluir = input_materias("¿Qué materias queres excluir? ")
    forzar = input_materias("¿Qué materias queres forzar? ")
    print("Calculando...")
    materias = set(materias).difference(set(excluir))
    combinaciones = get_combinaciones_posibles(materias, forzar, cantidad)
    guardar_output(combinaciones)


if __name__ == "__main__":
    main()