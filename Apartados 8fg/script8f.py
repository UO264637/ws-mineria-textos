import random

# ------------------------------------- APARTADO 8f -------------------------------------

f = open("noticias-no-negacionistas-etiquetadas.ndjson", "r",encoding="utf8")

lineas = f.readlines()

random.shuffle(lineas)

with open("10noticias.ndjson", "w",encoding="utf8") as file:
    for i, linea in enumerate(lineas):
        file.write(linea)
        if i == 9:
            break