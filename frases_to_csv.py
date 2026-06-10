# La función de este código es filtrar los enunciados de frases.csv
# para que no sea demasiado alto el número de enunciados y para 
# seleccionar solamente aquellos de una longitud definida.

import csv

with open('corpus/frases.txt', 'r', encoding='utf-8') as frases_file:
    frases = frases_file.read()

frases_string = []
frases_list = []
frase = []

# Filtrado de las frases
i = 0
for c in frases:
    if c != '\n':
        frase.append(c)
    else:
        frase_str = ''.join(frase)
        if (i % 4 == 1 and len(frase) >= 40 and len(frase) < 150):
            frases_string.append(frase_str)
            frases_list.append(frase_str.lower().split())
        frase = []
        i+=1


with open("corpus/frases1.csv",'w',encoding="utf-8",newline='') as csv_file:
    writer = csv.writer(csv_file)
    for i in range(len(frases_string)):
        writer.writerow([frases_string[i],frases_list[i]])
