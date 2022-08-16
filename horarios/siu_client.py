import requests
import os
from parse import parse_html
import json


def get_data():
    username = os.environ.get("USERNAME") or input("Usuario del SIU: ")
    password = os.environ.get("PASSWORD") or input("Contraseña del SIU: ")

    cookies = requests.post("https://guaraniautogestion.fi.uba.ar/g3w/acceso?auth=form", {
        "usuario": username,
        "password": password
    }, allow_redirects=False).cookies

    html = requests.get(
        "https://guaraniautogestion.fi.uba.ar/g3w/oferta_comisiones", cookies=cookies).text

    return parse_html(html)


if __name__ == "__main__":
    with open("data.json", "w", encoding="utf8") as f:
        json.dump(get_data(), f, ensure_ascii=False, indent=2)
