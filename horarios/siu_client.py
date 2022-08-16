import requests
import os
from parse import parse_html
import json

DIR = os.path.dirname(os.path.realpath(__file__))


def get_data():
    username = os.environ.get("SIU_USERNAME") or input("Usuario del SIU: ")
    password = os.environ.get("SIU_PASSWORD") or input("Contraseña del SIU: ")

    cookies = requests.post("https://guaraniautogestion.fi.uba.ar/g3w/acceso?auth=form", {
        "usuario": username,
        "password": password
    }, allow_redirects=False).cookies

    html = requests.get(
        "https://guaraniautogestion.fi.uba.ar/g3w/oferta_comisiones", cookies=cookies).text

    return parse_html(html)


"""
URL_MATERIAS_DISPONIBLES = "https://guaraniautogestion.fi.uba.ar/g3w/horarios_cursadas?formulario_filtro[ra]=3b5e0365f0c2299dfd89eb3852a8ebb566382194&formulario_filtro[carrera]=9220d714727dbe74790a6782a5241e56f7034064&formulario_filtro[anio_cursada]=&formulario_filtro[periodo]=29"
CODIGOS_DISPONIBLES =r"\( (\d\d\d\d) \)"
def get_materias_disponibles():
    response = requests.get(URL_MATERIAS_DISPONIBLES)
    return set(re.findall(CODIGOS_DISPONIBLES, response.text))
"""


if __name__ == "__main__":
    with open(DIR + "/data.json", "w", encoding="utf8") as f:
        json.dump(get_data(), f, ensure_ascii=False, indent=2)
