# Este código sirve para combinar los conjuntos de datos 10k_formas.txt con 
# embeddings.csv para producir el conjunto de datos emb_10k.csv
# del primero se toma la frecuencia de las palabras, mientras
# que del segundo se toman los embeddings. Solo se seleccionan
# las palabras que aparezcan en ambos conjuntos de datos

import csv
import pickle

num_palabras = 10000
rows = []

with open("10k_formas.txt",newline='',encoding="utf8") as formas_file:
    formas_file.readline()
    for i in range(num_palabras):
        rows.append(formas_file.readline().split())

for r in rows:
    r.pop(0)
    r.pop(1)

with open('vocab_to_int.pickle', 'rb') as f:
    vocab_to_int = pickle.load(f, encoding="utf8")

keys = vocab_to_int.keys()

filter_rows = filter(lambda a : a[0] in keys, rows)
rows = list(filter_rows)

num_palabras = len(rows)

embeddings = []
with open("embeddings.csv",'r',newline='') as emb_file:
    reader = csv.reader(emb_file)
    for row in reader:
        lst = []
        for a in row:
            lst.append(float(a))
        embeddings.append((lst))


with open("emb_10k.csv",'w',encoding="utf-8",newline='') as csv_file:
    writer = csv.writer(csv_file)
    for i in range(num_palabras):
        writer.writerow([rows[i][0],float(rows[i][1]),embeddings[vocab_to_int[rows[i][0]]]])

