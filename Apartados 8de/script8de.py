import pickle
import fasttext
import json
from collections import defaultdict

# ------------------------------------- CARGA DE DATOS -------------------------------------
with open('segmentos_no_negacionistas.pickle', 'rb') as handle:
  segmentos_no_negacionistas = pickle.load(handle)

clasificador = fasttext.load_model("clasificador.bin")
  
f = open("noticias-cambio-climático-españa-abril-2022-abril-2023-finales-sentencias-disagree-NOT-disagree.ndjson", "r",encoding="utf8")

lineas = f.readlines()

# ------------------------------------- APARTADO 8de -------------------------------------

textos = {}

def calcular_etiquetas(lista_etiquetas):
    contador_etiquetas = defaultdict(int)
    total_etiquetas = len(lista_etiquetas)
    porcentaje_etiquetas = {}

    for etiqueta in lista_etiquetas:
        contador_etiquetas[etiqueta[0]] += 1

    for etiqueta, contador in contador_etiquetas.items():
        porcentaje = (contador / total_etiquetas)
        porcentaje = round(porcentaje, 2)
        porcentaje_etiquetas[etiqueta] = porcentaje
    return porcentaje_etiquetas

with open("noticias-no-negacionistas-etiquetadas.ndjson", "w",encoding="utf8") as file:
    for linea in lineas:
        try:
            data = json.loads(linea.strip())
            if len(data["sentencias_disagree"])<len(data["sentencias_NOT_disagree"]):
                segmentos_noticia = segmentos_no_negacionistas[data["identifier"]]
                resultado = clasificador.predict(segmentos_noticia)
                data["etiquetas"] = calcular_etiquetas(resultado[0])

                file.write(json.dumps(data, ensure_ascii=False) + "\n") 
        except:
            pass

    
