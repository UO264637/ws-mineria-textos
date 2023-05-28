# Ejercicio de minería de textos
Ejercicio realizado por: Carmen Sirgo López - UO264637

Los puntos 1 al 6 con las noticias “negacionistas”. Los puntos 7 al 8 se realizarán con la colección contraria.


## Descarga del código
El código completo se puede descargar de este repositorio de GitHub: https://github.com/UO264637/ws-mineria-textos.git

## Datos
Los datos generados durante el desarollo de los ejercicios se encuentra en la carpeta /data para su consulta y evitar que sean sobreescritos al ejecutar los scripts.

## Instalación y despliegue
Para poder ejecutar este codigo es necesario seguir los siguientes pasos:
- Instalar Python 3.10 https://www.python.org/downloads/release/python-3108/
- Instalar los siguientes paquetes (para instalar spacy y textacy tuve que abrir la consola de comandos en modo administrador):
  -  pip install simhash
  -  pip install nltk
  -  pip install spacy
  -  pip install sklearn
  -  python -m spacy download es_core_news_sm
  -  pip install textacy
  -  pip install fasttext-wheel (fasttext me dio error e instalar pybind11 no lo solucionó: https://github.com/facebookresearch/fastText/issues/512)

Una vez instalados todos los paquetes necesarios deberán ejecutarse en orden los siguientes scripts ya que algunos de ellos dependen de la salida de los anteriores.
- script1-3.py: Contiene la solución de los apartados 1, 2 y 3
- script4.py: Contiene la solución del apartado 4
- script5-6.py: Contiene la solución de los apartados 5 y 6
- script8abc.py: Contiene la solución de los apartados 8a, 8b y 8c
- script8abc.py: Contiene la solución de los apartados 8d y 8e
- script8f.py: Contiene la solución del apartado 7f

## Desarrollo
A continuación, se documentará el contenido de los scripts anteriores y el proceso seguido para resolver el ejercicio:

### Apartado 1 - script1-3.py
Primero he detectado los documentos cuasi-duplicados utilizando el paquete simhash, para ello se crea una firma para cada documento y se comparan. He obtenido los siguientes resultados:
- Hay 63 documentos únicos.
- Hay 36 documentos que aparecen dos veces.
- Hay 6 documentos que aparecen 3 veces.
- Hay 4 documentos que aparecen 4 veces.
Después he escogido al azar uno de los documentos cuasi-duplicados y descartado el resto. Finalmente he obtenido 84 documentos no duplicados.


#### Apartado 2 - script1-3.py

En el mismo script he recorrido la lista de noticias no duplicadas para segmentarlas usando spaCy. Después uní los segmentos añadiendo un doble salto de líne entre cada uno de ellos para poder aplicar TextTiling.

Al aplicar TexTiling hubo algunos segmentos que daban error porque eran demasiado cortos para el algoritmo, tras consultarlo con el profesor, los descarté e imprimí un mesaje de error para cada uno de ellos.

Finalmente, tras aplicar TextTiling a cada segmento, eliminé los dobles saltos de línea y añadí todos los segmentos temáticos de cada noticia a una lista común. En total obtuve 548 segmentos.

### Apartado 3 - script1-3.py
Inicialmente probé a utilizar el algoritmo de affinity-propagation para hacer el clustering y obtuve alrededor de 120 clusteres, según la ejecución. Se puede ver un ejemplo en: [data/clusters-affinity-propagation.txt](https://github.com/UO264637/ws-mineria-textos/blob/main/data/clusters-affinity-propagation.txt). Sin embargo, echando un vistazo a los clusteres, me parecieron demasiados y algunos podrían ser agrupados, como el 81 y 82 que tratan del Apolo y viajes a la Luna.

Por esta razón decidí probar con el algoritmo de k-means, inicialmente con 60 clústeres: [data/clusters-k-means.txt](https://github.com/UO264637/ws-mineria-textos/blob/main/data/clusters-k-means.txt). Tras revisar los clústeres decidí incrementar el número a 70 porque había algunos clústeres como el 13 o el 22 que mezclaban temas muy distintos.

Decidí quedarme con 70 clústeres ([data/clusters-k-means-definitive.txt](https://github.com/UO264637/ws-mineria-textos/blob/main/data/clusters-k-means-definitive.txt)) porque las temáticas parecían bastante claras y, aunque había algunos clusteres que podrían agruparse (10-incendios y 11-superficie quemada) no era un número excesivo y me parecieron más sencillos de etiquetar.

En el mismo script (script1-3.py) vecroricé los seggmentos temáticos con TfidfVectorizer tras eliminar las palabras vacías con spacy. Después apliqué el algoritmo de k-means con 70 clústeres como mencioné anteriormente y almacené los clústeres y los segmentos con pickle en el siguiente script ya que los algoritmos de clústering tienen un componente aleatorio. Finalmente, guardé en un .txt el resultado del clustering con algunos fragmentos de los segmentos de cada clúster para poder etiquetarlos manualmente.

### Apartado 4
A continuación, etiqueté manualmente los clústeres que me parecieron más prometedores. Se puede encontrar en: [labels.txt](https://github.com/UO264637/ws-mineria-textos/blob/main/data/labels.txt).

Algunos clústeres como el 29 tenían temáticas claras (viajes a la Luna en este caso) pero que no estaban relacionadas con el medio ambiente por lo que los marqué como __label__offtopic.

### Apartado 5 - script5-a.py
En este script cargo los datos de los archivos .pickle y agrupo los segmentos temáticos en cada clúster correspondeinte. Después, si el clúster está etiquetado, añado la etiqueta a todos sus segmentmentos y los escribo en un fichero [labeled-segments.txt](https://github.com/UO264637/ws-mineria-textos/blob/main/data/labeled-segments.txt) de forma que cada segmento no tiene saltos de línea y en cada línea del fichero aparece cada segmento con su etiqueta delante. Este fichero se utilizará para crear los conjuntos de testing y entrenamiento en el ejercicio siguiente para entrenar el clasificador.

### Apartado 6 - script5-6.py
En este script divido los segmentos etiquetados en dos grupos de test y training de forma aleatoria (20% y 80% respectivamente). Inicialmente me salió un clasificador muy malo, alrededor de un 10% de precisión. Creo que esto se debe a que el conjunto de datos es muy pequeño así que traté de procesar los datos para intentar mejorar el clasificador.

Utilicé nltk para tokenizar el textó y normalizarlo, lo que mejoró ligeramente el clasificador (entre un 5 y un 10%). Sin embargo, cuando probé a eliminar las palabras vacías el clasificador era incluso peor que al principio por lo que decídí no hacerlo.

Probé a eliminar los signos te puntuación utilizando "re" y conseguí que el clasificador alcanzara un 30% de precisión en algunas ocasiones. Creo que la precision varía mucho de una ejecución a otra debido a que son pocos datos y la creción aleatoria de los grupos de testing y training puede cambiar mucho los resultados.

Probé distintos valores para epoch y learning rate pero con tan pocos datos me daba miedo estar sobreajustando el modelo si ponía un epoch muy elevado por lo que al final establecí un epoch de 30 y un learning rate de 1.0. Con estos valores obtenía una precisión de entre 70% y 90% en la mayoría de casos.

El clasificador que he utilizado a partir de aquí tiene una precisión de : [clasificador.bin](https://github.com/UO264637/ws-mineria-textos/blob/main/data/clasificador.bin)

### Apartado 8
#### Apartados 8 a, b y c - script8abc.py
Como este conjunto tiene muchas más noticias la ejecución lleva varios minutos, así que decidí hacer estos pasos en un script independiente del etiquetado.

Repetí los pasos del apartado 2 para la colección de noticias "no negacionistas" pero incluí la normalización del texto y eliminé los signos de puntiación para que tuviera el mismo formato que los datos utilizados para entrenar el clasificador. Almacené los segmentos agrupados por noticia con pickle para poder calcular los porcentajes más adelante: [data/segmentos_no_negacionistas.pickle](https://github.com/UO264637/ws-mineria-textos/blob/main/data/segmentos_no_negacionistas.pickle)

#### Apartados 8 d y e - script8de.py
En este script etiqueto los segmentos de cada noticia generados con el script anterior. Después, calculo el porcentaje de segmentos de la noticia que pertenecen a cada etiqueta mediante la funcion "calcular_etiquetas" y añado esta información a los datos de las noticiass antes de almacenarlo en un archivo ndjson. [noticias-no-negacionistas-etiquetadas.ndjson](https://github.com/UO264637/ws-mineria-textos/blob/main/data/noticias-no-negacionistas-etiquetadas.ndjson)

#### Apartados 8 f - script8f.py
He creado un pequeño script para seleccionar 10 noticias aleatorias del archivo anterior. Se pueden encontrar en: [10noticias.ndjson](https://github.com/UO264637/ws-mineria-textos/blob/main/data/10noticias.ndjson)




