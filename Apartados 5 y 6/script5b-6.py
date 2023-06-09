# pip install pybind11 no funciono
# pip install fasttext-wheel https://github.com/facebookresearch/fastText/issues/512

import fasttext
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# ------------------------------------- APARTADO 5 -------------------------------------

# Tokenización y normalización del texto para tratar de mejorar el clasificador

nltk.download('punkt')
stop_words = set(stopwords.words('spanish')) 

labeled_segments = []
with open("labeled-segments.txt", encoding='utf-8') as file:
    for line in file:
        tokens = word_tokenize(line)
        # tokens_filtrados = [token for token in tokens if token.lower() not in stop_words]
        tokens_normalizados = [token.lower() for token in tokens]
        texto_preprocesado = ' '.join(tokens_normalizados)
        texto_sin_puntuacion = re.sub(r'[^\w\s]', '', texto_preprocesado)
        labeled_segments.append(texto_sin_puntuacion+"\n")


# Crear conjuntos de testing y entrenamiento

random.shuffle(labeled_segments)

divider = len(labeled_segments)//10*2 # 20% test 80% training
test = labeled_segments[:divider]
training = labeled_segments[divider:]

with open("test-segments.txt", "w", encoding='utf-8') as file:
    for segment in test:
       file.write(segment)

with open("training-segments.txt", "w", encoding='utf-8') as file:
    for segment in training:
       file.write(segment)


# ------------------------------------- APARTADO 6 -------------------------------------

clasificador = fasttext.train_supervised("labeled-segments.txt", epoch=30, lr=1.0) #wordNgrams=2,

def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*clasificador.test('test-segments.txt'))
results = clasificador.test('test-segments.txt')

clasificador.save_model("clasificador.bin")