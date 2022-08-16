# Calculadora de materias

Descarga los horarios del SIU y calcula todas las posibles combinaciones de cursos que se pueden hacer (sin superposición) a partir de las materias aprobadas hasta el momento. El repositorio cuenta con los datos de la carrera de Ingeniería Informática (ver sección de [horarios](#horarios) y [plan](#plan-de-estudios)).

Uso:

1. Instalar las dependencias (`pip3 install -r requirements.txt`, opcionalmente con un `venv`)
2. Crear un archivo `aprobadas.txt` con el código de las materias que ya se aprobaron en cada línea
3. Ejecutar `python3 main.py`.

> El periodo lectivo a utilizar se configura en la constante `PERIODO` en `calculadora.py`

> La lógica para obtener las combinaciones está en `calculadora.py`. El archivo `main.py` es simplemente una CLI de sus utilidades.

## Horarios

La carpeta `horarios` contiene el código para descargar el plan de estudios desde el SIU y un archivo `data.json` con los horarios del primer y segundo cuatrimestre de 2022 de los cursos de la carrera de Ingeniería Informática (obtenidos con el mismo código, solamente agregándole los cursos de Compiladores y Tecnologías Emergentes que no se encuentran en el SIU).

Se decidió obtener los horarios desde el SIU y no desde `https://ofertahoraria.fi.uba.ar/` ya que el el SIU suele ser el primero en actualizarse, pudiendo el segundo demorar varios días en hacerlo. La desventaja es que requiere autenticarse con las credenciales de un alumno de la carrera de la que se busca obtener la oferta horaria.

Uso:

1. `python3 horarios/siu_client.py`

La herramienta va a pedir usuario y contraseña del SIU para acceder a la pestaña de Oferta de Comisiones. También se pueden guardar las credenciales en las variables de entorno `SIU_USERNAME` y `SIU_PASSWORD` para que no se pidan cada vez que se ejecuta.

## Plan de estudios

La carpeta `plan` contiene el código para parsear el plan de estudios de una carrera a partir de un archivo de texto en el que se copiaron y pegaron las materias directamente desde el pdf del plan de estudios (ver `plan/raw.txt`).

El archivo `data.json` contiene todos los cursos del plan de estudios de Ingenería en Informática actualizado a 2022 (obtenidos con el mismo código, solamente agregándole las materias de Compiladores y Tecnologías Emergentes que no se encuentran en el plan).

Uso:

1. Copiar y pegar desde el pdf del plan de estudios todas las materias a un archivo de texto `raw.txt` en el directorio `plan`. Asegurarse que cada materia ocupe una línea (algunas con nombre largo puede que queden en 2).
2. Actualizar la constante `CREDITOS_PLAN` en `plan/parse.py` de acuerdo a la cantidad de créditos necesaria para recibirse del plan de estudios a parsear.
3. Ejecutar `python3 plan/parse.py`, lo cual generará el archivo `data.json`.
