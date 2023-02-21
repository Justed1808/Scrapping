print('Jeu de la vie :')

import random as rd
t = []
for i in range(1, 10):
    nvline = []
    for j in range(1, 5):
        nvline.append(rd.randint(0,1))
    t.append(nvline)

m = 0
v = 0

for lo in t:
    for el in lo:
        if(el == 0):
            print(".", end = "")
            m = m + 1
        else:
            print("O", end = "")
            v = v + 1
        print("", end ="\t")
    print()

print(v)
print(m)


#Initialisation des variables

#Définir la largeur (x) et la longueur de mon tableau a 2 dimensions

#Créer une fonciton qui me génère et renvoit un tableau a 2 dimensions, remplit de cellules mortes ou vivantes

#Créer une fonction qui itère sur chaque cellule du tableau (ligne par ligne puis colonne pa colonne)

#Créer une fonction qui vérifie les voisins d'une cellule

