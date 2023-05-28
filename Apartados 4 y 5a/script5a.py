import pickle
import random

# ------------------------------------- APARTADO 5 -------------------------------------

# Carga de datos
with open('clustering.pickle', 'rb') as handle:
  clustering = pickle.load(handle)

with open('segments.pickle', 'rb') as handle:
  segmentos_tematicos = pickle.load(handle)

cluster_labels = {}
with open("labels.txt") as f:
    for line in f:
       (key, val) = line.split(" ")
       cluster_labels[int(key)] = val.replace("\n","")

# Agrupar segmentos por cluster

clustered_docs1 = dict()
docs_per_cluster1 = dict()

for i in range(len(clustering.labels_)):
  try:
    clustered_docs1[clustering.labels_[i]].append(i)
    docs_per_cluster1[clustering.labels_[i]]+=1
  except:
    clustered_docs1[clustering.labels_[i]] = list()
    clustered_docs1[clustering.labels_[i]].append(i)
    docs_per_cluster1[clustering.labels_[i]]=1

ids = list(docs_per_cluster1.keys())
ids.sort()
sorted_docs_per_cluster1 = {i: docs_per_cluster1[i] for i in ids}

# Los segmentos no pueden tener saltos de línea y cada par etiqueta, segmento debe estar separado por un salto de línea

with open("labeled-segments.txt", "w", encoding='utf-8') as file:
    for cluster_id in sorted_docs_per_cluster1:
        if (cluster_id in cluster_labels):
          ejemplares = clustered_docs1[cluster_id]
          for ejemplar in ejemplares:
            file.write(cluster_labels[cluster_id] + segmentos_tematicos[ejemplar].replace("\n"," ") + "\n") 