# Este código genera el archivo 'frases.csv' Contiene los enunciados junto
# a la lista de las palabras que los componen.
with open ('corpus/text.txt', 'r', encoding='utf-8') as f:
    spanishText = f.read()

#En esta parte se rellena la lista frases con las frases
#encontradas en el texto del corpus.
frase_empezada = False
c_anterior = 'c'
frases = []
frase = []
for c in spanishText:
    if c in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z','¿','¡']:
        frase_empezada = True
    if frase_empezada:
        frase.append(c)
    if c == '.' and frase_empezada and c_anterior == ' ':
        frases.append(frase)
        frase = []
        frase_empezada = False
    if c == '@' or c == '=' or c == '#' or c == '\\':
        frase = []
        frase_empezada = False


    c_anterior = c

with open ('corpus/frases.txt', 'w', encoding='utf-8') as f:
    for fr in frases:
        f.write(''.join(fr))
        f.write('\n')