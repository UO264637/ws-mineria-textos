import json
from collections import Counter
from simhash import Simhash, SimhashIndex
import random
import spacy
import nltk
nltk.download("stopwords")
from nltk.tokenize import TextTilingTokenizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from collections import OrderedDict
import pickle

# ------------------------------------- CARGA DE DATOS -------------------------------------
f = open("noticias-cambio-climático-españa-abril-2022-abril-2023-finales-sentencias-disagree-NOT-disagree.ndjson", "r",encoding="utf8")
lineas = f.readlines()
textos = list()

for linea in lineas:
    try:
      data = json.loads(linea)
      if len(data["sentencias_disagree"])>len(data["sentencias_NOT_disagree"]): # Noticias negacionistas
        texto = " ".join(data["sentencias"])
        texto = "".join(texto.splitlines())
        textos.append(texto)
    except:
      pass

# ------------------------------------- APARTADO 1 -------------------------------------
firmas = []
valor_f = 128
observaciones = []

# Creamos las firma de cada documento

for i in range(len(textos)):
    texto = textos[i]

    firma = Simhash(texto, f=valor_f)
    firmas.append((i,firma)) 

indice = SimhashIndex(firmas, k=10, f=valor_f)

# Determinamos cuántos duplicados hay en la colección

for i in range(len(textos)):
    firma = firmas[i][1]
    duplicados = indice.get_near_dups(firma)

    observaciones.append(len(duplicados))

print()
print(Counter(observaciones).most_common(50))

textos_no_duplicados = list()
ignorar = list()

for i in range(len(textos)):
    if i not in ignorar:
      texto = textos[i]

      firma = firmas[i][1]

      duplicados = indice.get_near_dups(firma)

      if len(duplicados)==1:
        textos_no_duplicados.append(texto)
        ignorar.append(i)
      else:
        random.shuffle(duplicados)

        ident = int(duplicados[0])
        
        textos_no_duplicados.append(textos[ident])
        for ident in duplicados:
          ignorar.append(int(ident))


print()
print("Textos no duplicados: " + str(len(textos_no_duplicados)))
print()

# ------------------------------------- APARTADO 2 -------------------------------------
segmentos_tematicos = list()
# Parseamos el texto con spaCy, segmentamos en sentencias, convertimos los spans que genera spaCy en cadenas de texto
nlp = spacy.load("es_core_news_sm")

stopwords_spanish = set(stopwords.words('spanish'))

tt = TextTilingTokenizer(stopwords=stopwords_spanish)

for noticia in textos_no_duplicados:
    doc = nlp(noticia)

    sentencias = list(doc.sents)

    for i in range(len(sentencias)):    
        sentencias[i] = sentencias[i].text

    texto = "\n\n".join(sentencias)

    # Segmentamos el texto utilizando el algoritmo TextTiling (algunos segmentos son demasiado cortos y da error)
    try:
        segments = tt.tokenize(texto)
        for i in range(len(segments)):
            segment = segments[i]
            segment = segment.replace("\n\n","\n")
            segmentos_tematicos.append(segment)

    except Exception as e:
       print("ERROR: " , end="")
       print(e)

print()   
print("Seggmentos tematicos: " + str(len(segmentos_tematicos)))
print()   


# ------------------------------------- APARTADO 3 -------------------------------------

# Vectorización de los documentos
nlp = spacy.load("es_core_news_sm")
stop_words = list(spacy.lang.es.stop_words.STOP_WORDS)

vectorizador = TfidfVectorizer(encoding="utf-8", lowercase=True,
                               stop_words=stop_words, ngram_range=(1,3), 
                               max_features=10000)

doc_term_matrix = vectorizador.fit_transform(segmentos_tematicos)

# El número de clusters debe fijarse de antemano
num_clusters = 70
clustering1 = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=1000, n_init=1, verbose=True)

# Se aplica el algoritmo seleccionado a la matriz que representa el corpus

clustering1.fit(doc_term_matrix)

# Se guarda el clustering y los seggmentos para poder etiquetarlos en el siguiente script
with open('clustering.pickle', 'wb') as handle:
  pickle.dump(clustering1, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('segments.pickle', 'wb') as handle:
  pickle.dump(segmentos_tematicos, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Se imprimen los clusters en un formato legible mostrando un fragmento de cada segmento temático para poder hacer la ettiquetación manual
clustered_docs1 = dict()
docs_per_cluster1 = dict()

for i in range(len(clustering1.labels_)):
  try:
    clustered_docs1[clustering1.labels_[i]].append(i)
    docs_per_cluster1[clustering1.labels_[i]]+=1
  except:
    clustered_docs1[clustering1.labels_[i]] = list()
    clustered_docs1[clustering1.labels_[i]].append(i)
    docs_per_cluster1[clustering1.labels_[i]]=1

ids = list(docs_per_cluster1.keys())
ids.sort()
sorted_docs_per_cluster1 = {i: docs_per_cluster1[i] for i in ids}

terminos = vectorizador.get_feature_names_out()

indice_cluster_terminos1 = clustering1.cluster_centers_.argsort()[:, ::-1]

with open("clusters-k-means.txt", "w", encoding='utf-8') as file:
    for cluster_id in sorted_docs_per_cluster1:
        # Escribe el encabezado del cluster en el archivo
        file.write("Cluster %d (%d documentos): " % (cluster_id, docs_per_cluster1[cluster_id]))

        for term_id in indice_cluster_terminos1[cluster_id, :10]:
            # Verifica si el valor no es nulo
            if clustering1.cluster_centers_[cluster_id][term_id] != 0:
                file.write('"%s" ' % terminos[term_id])

        ejemplares = clustered_docs1[cluster_id]
        random.shuffle(ejemplares)
        for ejemplar in ejemplares[0:5]:
            file.write("\t" + segmentos_tematicos[ejemplar][0:140] + "...")

        file.write("\n")
        file.write("\n")

"""
clustering2 = AffinityPropagation(damping=0.9, max_iter=1000, verbose=True)
clustering2.fit(doc_term_matrix)

cluster_labels_to_indexes = dict()
for i in range(len(clustering2.cluster_centers_indices_)):
  label = clustering2.cluster_centers_indices_[i]
  cluster_labels_to_indexes[label] = i

docs_per_cluster2 = OrderedDict(Counter(clustering2.labels_))

print("Número de clusters descubiertos: %d" % len(docs_per_cluster2))

clustered_docs2 = dict()
docs_per_cluster2 = dict()

for i in range(len(clustering2.labels_)):
  try:
    clustered_docs2[clustering2.labels_[i]].append(i)
    docs_per_cluster2[clustering2.labels_[i]]+=1
  except:
    clustered_docs2[clustering2.labels_[i]] = list()
    clustered_docs2[clustering2.labels_[i]].append(i)
    docs_per_cluster2[clustering2.labels_[i]]=1

ids = list(docs_per_cluster2.keys())
ids.sort()
sorted_docs_per_cluster2 = {i: docs_per_cluster2[i] for i in ids}

terminos = vectorizador.get_feature_names_out()

cluster_centers2 = clustering2.cluster_centers_.toarray()

indice_cluster_terminos2 = cluster_centers2.argsort()[:, ::-1]


with open("clusters-affinity-propagation.txt", "w", encoding='utf-8') as file:

    for cluster_id in docs_per_cluster2:
        file.write("Cluster %d (%d documentos): " % (cluster_id, docs_per_cluster2[cluster_id]))

        for term_id in indice_cluster_terminos2[cluster_id, :10]:
            if cluster_centers2[cluster_id][term_id] != 0:
                file.write('"%s" ' % terminos[term_id])

        ejemplares = clustered_docs2[cluster_id]
        random.shuffle(ejemplares)
        for ejemplar in ejemplares[0:5]:
            file.write("\t%s ..." % segmentos_tematicos[ejemplar][0:140])

        file.write("\n")
        file.write("\n")
"""