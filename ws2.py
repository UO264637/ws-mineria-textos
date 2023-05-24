import pickle
import random

with open('clustering.pickle', 'rb') as handle:
  clustering = pickle.load(handle)

with open('segments.pickle', 'rb') as handle:
  segmentos_tematicos = pickle.load(handle)

print(clustering)

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

#terminos = vectorizador.get_feature_names_out()

indice_cluster_terminos1 = clustering.cluster_centers_.argsort()[:, ::-1]

with open("clusters-pickle.txt", "w", encoding='utf-8') as file:
    for cluster_id in sorted_docs_per_cluster1:
        # Escribe el encabezado del cluster en el archivo
        file.write("Cluster %d (%d documentos): " % (cluster_id, docs_per_cluster1[cluster_id]))

        ejemplares = clustered_docs1[cluster_id]
        random.shuffle(ejemplares)
        for ejemplar in ejemplares[0:5]:
            file.write("\t" + segmentos_tematicos[ejemplar][0:140] + "...")

        file.write("\n")
        file.write("\n")