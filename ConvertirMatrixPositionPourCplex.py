import tkinter as tk
from tkinter import filedialog 
import math


def ouvrirFichier():
    lignes =[]
    fichier=filedialog.askopenfilename()
    if fichier:
        with open(fichier, 'r') as file:
            for line in file:
                lignes.append(line.strip())

    VehicleCapa = lignes[1].split()
    nbVehicule = len(VehicleCapa)
    depot=lignes[2].split()

    tableauPosition=[[depot[0],depot[1]]]
    tableauCapa=['0']
    for indice, valeur in enumerate(lignes[3:], start=3):
        tmp =valeur.split()
        tableauPosition.append([tmp[1],tmp[2]])
        tableauCapa.append(tmp[3])

    tableauDistance=[]
    for lignes in tableauPosition:
        lignetmp=lignes
        tableauDistanceTmp=[]
        for ligne in tableauPosition:
            tableauDistanceTmp.append(round(math.sqrt((float(ligne[0]) - float(lignetmp[0]))**2+ (float(ligne[1])-float(lignetmp[1]))**2 ),2))
        tableauDistance.append(tableauDistanceTmp)

    strdistance='d=['
    for dis in tableauDistance:
        strdistance+='['
        for d in dis:
            strdistance+=str(d)
            strdistance+=' '
        strdistance=strdistance[:-1]
        strdistance+='],'
    strdistance=strdistance[:-1]
    strdistance+='];'

    strCapa='c=['
    for c in tableauCapa:
        strCapa+=str(c)
        strCapa+=','
    strCapa=strCapa[:-1]
    strCapa+='];'

    fichierecrit = fichier[:-3]
    fichierecrit+='.dat'
    with open(fichierecrit, 'w') as file:
        file.write(strdistance)
        file.write('\n')
        file.write('\n')
        file.write(strCapa)




fenetre=tk.Tk()
ouvrirButton=tk.Button(fenetre, text="Selectionner un fichier", command=ouvrirFichier())
ouvrirButton.pack()
fenetre.mainloop()
