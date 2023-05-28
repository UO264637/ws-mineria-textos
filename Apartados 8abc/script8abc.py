import json
import spacy

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TextTilingTokenizer
import pickle
import re

# ------------------------------------- CARGA DE DATOS -------------------------------------
f = open("noticias-cambio-climático-españa-abril-2022-abril-2023-finales-sentencias-disagree-NOT-disagree.ndjson", "r",encoding="utf8")

lineas = f.readlines()

textos = {}

for linea in lineas:
    try:
      data = json.loads(linea)
      if len(data["sentencias_disagree"])<len(data["sentencias_NOT_disagree"]):
        identificador = data["identifier"]
        texto = " ".join(data["sentencias"])
        texto = "".join(texto.splitlines())
        textos[identificador] = texto
    except:
      pass


# ------------------------------------- APARTADO 8abc -------------------------------------
segmentos_tematicos = {}
# Parseamos el texto con spaCy, segmentamos en sentencias, convertimos los spans que genera spaCy en cadenas de texto
nlp = spacy.load("es_core_news_sm")

stopwords_spanish = set(stopwords.words('spanish'))

tt = TextTilingTokenizer(stopwords=stopwords_spanish)

for identificador, texto in textos.items():
    doc = nlp(texto)

    sentencias = list(doc.sents)

    for i in range(len(sentencias)):    
        sentencias[i] = sentencias[i].text

    texto = "\n\n".join(sentencias)

    # Segmentamos el texto utilizando el algoritmo TextTiling
    try:
        segments = tt.tokenize(texto)
        segmentos = list()
        for i in range(len(segments)):
            segment = segments[i]
            segment = segment.replace("\n\n","\n")

            # Procesado del texto 
            tokens = word_tokenize(segment)
            tokens_normalizados = [token.lower() for token in tokens]
            texto_preprocesado = ' '.join(tokens_normalizados)
            texto_sin_puntuacion = re.sub(r'[^\w\s]', '', texto_preprocesado)

            segmentos.append(texto_sin_puntuacion)
        segmentos_tematicos[identificador] = segmentos # Segmentos agrupados por noticia

    except Exception as e:
       print("ERROR")
       print(e)

    
print(len(segmentos_tematicos))

with open('segmentos_no_negacionistas.pickle', 'wb') as handle:
  pickle.dump(segmentos_tematicos, handle, protocol=pickle.HIGHEST_PROTOCOL)