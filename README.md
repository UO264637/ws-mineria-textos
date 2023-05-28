# Ejercicio de minería de textos
Ejercicio realizado por: Carmen Sirgo López - UO264637

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
- script1-3.py: Contiene la solución de los apartados 1, 2 y 4
- script4.py: Contiene la solución del apartado 4
- script5-6.py: Contiene la solución de los apartados 5 y 6
- script8abc.py: Contiene la solución de los apartados 8a, 8b y 8c
- script8abc.py: Contiene la solución de los apartados 8d y 8e
- script8f.py: Contiene la solución del apartado 7f

## Desarrollo
A continuación, se documentará el contenido de los scripts anteriores y el proceso seguido para resolver el ejercicio:
### 1. Eliminar documentos cuasi-duplicados de la colección de trabajo.
Primero he detectado los documentos cuasi-duplicados utilizando el paquete simhash, para ello se crea una firma para cada documento y se comparan. He obtenido los siguientes resultados:
- Hay 63 documentos únicos.
- Hay 36 documentos que aparecen dos veces.
- Hay 6 documentos que aparecen 3 veces.
- Hay 4 documentos que aparecen 4 veces.
Después he escogido al azar uno de los documentos cuasi-duplicados y descartado el resto. Finalmente he obtenido 84 documentos no duplicados.



### 2. Para cada una de las noticias únicas hacer lo siguiente: 
####     a. Segmentar la noticia en sentencias usando spaCy.
####     b. Unir esas sentencias en un único texto de tal modo que entre sentencia y sentencia haya un doble salto de línea \n\n.
####     c. Usar TextTiling con ese texto para obtener segmentos temáticamente coherentes.
####     d. Añadir todos los segmentos a una lista única para la colección.

En el mismo script he recorrido la lista de noticias no duplicadas para segmentarlas usando spaCy. Después uní los segmentos añadiendo un doble salto de líne entre cada uno de ellos para poder aplicar TextTiling.

Al aplicar TexTiling hubo algunos segmentos que daban error porque eran demasiado cortos para el algoritmo, tras consultarlo con el profesor, los descarté e imprimí un mesaje de error para cada uno de ellos.

Finalmente, tras aplicar TextTiling a cada segmento, eliminé los dobles saltos de línea y añadí todos los segmentos temáticos de cada noticia a una lista común. En total obtuve 548 segmentos.

### 3. Aplicar clustering (el algoritmo que prefieras) a los segmentos obtenidos para toda la colección.
Inicialmente probé a utilizar el algoritmo de affinity-propagation para hacer el clustering y obtuve alrededor de 120 clusteres, según la ejecución. Se puede ver un ejemplo en: []


Seleccionar manualmente aquellos clusters que resulten más prometedores por los términos y los documentos representativos. Asignarles una etiqueta autodescriptiva (p.ej., “sequía”, “ola de calor”, “incendio”, “temperaturas extremas”, “carbón”, “hidrógeno”, etc.) En caso de duda, contactar con dani@uniovi.es para consensuar una etiqueta.
Crear con los documentos de esos clusters y las etiquetas aportadas manualmente un conjunto de entrenamiento y otro de test para un clasificador. ¡Atención! El clasificador no es multi-etiqueta puesto que cada segmento debería tratar única y exclusivamente de un tema principal (después de todo es el objetivo de TextTiling).
Entrenar y evaluar dicho clasificador.
A partir de aquí tomar la colección con la que no se trabajó (es decir, si la última cifra de tu DNI es par te toca “no negacionistas” y si es impar “negacionistas”).
Para cada noticia de esta segunda colección:
Segmentar en sentencias con spaCy.
Unir esas sentencias en un único texto con un doble salto de línea \n\n entre sentencias.
Usar TextTiling para segmentar ese texto en segmentos temáticamente coherentes.
Usar el clasificador anterior del punto 6 para asignar una temática a cada segmento.
Generar un archivo ndjson que contenga la información disponible sobre cada noticia de esta segunda colección además de un campo “etiquetas” donde se indique el % de segmentos de la noticia que correspondan a cada etiqueta determinada por el clasificador—p.ej. “etiquetas”: {“sequía”: 0.05, “ola_calor”: 0.25, “incendio”: 0.50, “temperaturas_extremas”: 0.1}
Seleccionar aleatoriamente 10 noticias de ese archivo y (sin mirar las etiquetas asignadas por el clasificador) etiquetarlas manualmente.
Comparar los resultados del etiquetado manual y automático y valorarlos en términos de precisión (global y por etiqueta).

