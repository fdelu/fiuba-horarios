import json
import os
from itertools import combinations, product, starmap
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock

DIR = os.path.dirname(os.path.realpath(__file__))
PATH_CURSOS = DIR + "/horarios/data.json"
PATH_PLAN = DIR + "/plan/data.json"
PERIODO = "2022 - 2do cuatrimestre"

with open(PATH_PLAN, "r", encoding="utf8") as f:
    PLAN = json.load(f)
    PLAN = {x["codigo"]: x for x in PLAN}

with open(PATH_CURSOS, "r", encoding="utf8") as f:
    CURSOS = json.load(f)[PERIODO]


def get_creditos(materias):
    creditos = 0
    for materia in materias:
        creditos += PLAN[materia]["creditos"]
    return creditos


def es_idioma(materia):
    return "idioma" in PLAN[materia]["nombre"].lower()


def get_materias_posibles(materias_aprobadas):
    creditos = get_creditos(materias_aprobadas)

    aprobo_idioma = any(es_idioma(materia) for materia in materias_aprobadas)

    posibles = set()
    for codigo, info in PLAN.items():
        if not all(map(lambda x: x in materias_aprobadas, info["correlativas"])) \
                or info["min_creditos"] > creditos \
                or codigo in materias_aprobadas \
                or (aprobo_idioma and es_idioma(codigo)):
            continue
        posibles.add(codigo)

    return posibles


def get_materias_disponibles():
    return CURSOS.keys()


def _horas_overlap(horas_1, horas_2):
    return max(horas_1["inicio"], horas_2["inicio"]) < min(horas_1["fin"], horas_2["fin"])


def _cursos_overlap(cursos):
    for curso_1, curso_2 in combinations(cursos, 2):
        for dia in set(curso_1["horarios"].keys()).intersection(set(curso_2["horarios"].keys())):
            for horas_1, horas_2 in product(curso_1["horarios"][dia], curso_2["horarios"][dia]):
                if _horas_overlap(horas_1, horas_2):
                    return True
    return False


def _comprobar_materias(materias, lock, posibles):
    for cursos in product(*map(lambda x: CURSOS[x], materias)):
        if not _cursos_overlap(cursos):
            lock.acquire()
            posibles.append(zip(materias, cursos))
            lock.release()


def get_combinaciones_posibles(opciones, forzadas, cantidad):
    print(opciones)
    resto = set(opciones).difference(set(forzadas))
    comb_resto = combinations(resto, cantidad - len(forzadas))
    if forzadas:
        total = starmap(lambda x, y: (*x, *y), product(forzadas, comb_resto))
    else:
        total = comb_resto
    posibles = []
    lock = Lock()
    with ThreadPoolExecutor() as threadpool:
        futures = []
        for materias in total:
            futures.append(threadpool.submit(
                _comprobar_materias, materias, lock, posibles))
        wait(futures)

    return posibles
