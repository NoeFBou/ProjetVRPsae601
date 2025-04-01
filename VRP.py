import os
import tkinter as tk
from tkinter import ttk 
import cplex
import math

tabcoulour=['brown','blue4','dark green','indianred','purple4', 'salmon4','PaleGreen4', 'chartreuse','']
tab=[]
selected_file=''

def flecheVille(canvas, x1, y1, x2, y2, voiture):
    canvas.create_line(float(x1)*7-5+50, float(y1)*7+50, float(x2)*7+50, float(y2)*7+50, arrow=tk.LAST, fill=tabcoulour[int(voiture)], width=3)


def ihm(selected_file, data, affichage):
    selected_file=selected_file[:-3]+'.txt'


    with open(os.path.join("./donnees/", selected_file)) as file:
        lignes=file.readlines()
    VehicleCapa = lignes[1].split()
    nbVehicule = len(VehicleCapa)
    depot=lignes[2].split()

    tableauPosition=[[depot[0],depot[1]]]
    tableauCapa=[]
    for indice, valeur in enumerate(lignes[3:], start=3):
        tmp =valeur.split()
        tableauPosition.append([tmp[1],tmp[2]])
        tableauCapa.append(tmp[3])
    
    root= tk.Tk()
    root.title("Affichage Cplex")
    canvas = tk.Canvas(root, width=1000,height=800)
    canvas.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

    # Création du cadre à droite
    right_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Ajout d'un widget Label dans le cadre droit
    right_label = tk.Label(right_frame, text=affichage)
    right_label.pack(padx=10, pady=10)
        
    tableauDistance=[]
    for lignes in tableauPosition:
        lignetmp=lignes
        tableauDistanceTmp=[]
        for ligne in tableauPosition:
            tableauDistanceTmp.append(round(math.sqrt((float(lignetmp[1])- float(lignetmp[0]))**2+ (float(ligne[1])-float(ligne[0]))**2 ),2))
        tableauDistance.append(tableauDistanceTmp)

        nodes = tableauPosition

        for i in range(0,len(nodes)):
            canvas.create_oval(float(nodes[i][0])*7-6+50,float(nodes[i][1])*7-6+50,float(nodes[i][0])*7+6+50,float(nodes[i][1])*7+6+50,fill="grey")
            if i==0:
                canvas.create_text(float(nodes[i][0])*7+50,float(nodes[i][1])*7-15+50,text='depot')
            else:
                canvas.create_text(float(nodes[i][0])*7+50,float(nodes[i][1])*7-15+50,text='client '+str(i))
        

        for trajets in data:
            flecheVille(canvas,nodes[int(trajets[0])][0],nodes[int(trajets[0])][1],nodes[int(trajets[1])][0],nodes[int(trajets[1])][1], trajets[2])
    
    root.mainloop() 

# Fonction pour résoudre le fichier LP sélectionné
def run_selected_lp():
    selected_file = lp_files_combobox.get()
    if selected_file:
        try:
            print(selected_file)
            # Utilisation de l'API CPLEX pour lire et résoudre le fichier LP sélectionné
            c = cplex.Cplex()
            file_path = os.path.join("./donnees", selected_file)  # Chemin complet du fichier LP
            c.read(file_path)
            c.solve()
            affichage=""

            print("Solution pour ", selected_file[:-3], "\n")
            affichage+=str("Solution pour ")+ str(selected_file[:-3] + "\n\n")
            for i, value in enumerate(c.solution.get_values()):
                if value != 0:
                    names = c.variables.get_names(i).replace("#", " ");
                    tmp = names.split(" ")
                    tab.append(tmp)
                else:
                    continue

            trajets = [item[1:] for item in tab if item[0] == 'x']
                            
            affichage+=affichageConsole(trajets)
            
            print("Valeur de la fonction objectif", round(c.solution.get_objective_value(),2))
            affichage+= str("Valeur de la fonction objectif : " + str(round(c.solution.get_objective_value(),2)))

            ihm(selected_file, trajets, affichage)

        except cplex.exceptions.CplexError as e:
            print("Aucunes solution trouvé", e)
    else:
        print("Aucun fichier sélectionné.")

# Fonction pour remplir la liste déroulante avec les fichiers LP du dossier 'donnees'
def browse_directory(event):
    folder_path = "./donnees"  # Chemin du dossier "donnees"
    if folder_path:
        lp_files = [f for f in os.listdir(folder_path) if f.endswith(".lp")]
        lp_files_combobox['values'] = lp_files


def trouver_trajets(depart, tableau_trie, numVoiture):
    text = ""
    for trajet in tableau_trie:
        if trajet[0] == depart:
            if trajet[0] == 0 and trajet[1] == 0:
                print("La voiture ", numVoiture, " reste au dépôt", "\n")
                text += "La voiture " + str (numVoiture) + " reste au dépôt" + "\n"
            elif trajet[1] == 0:
                print("La voiture ", numVoiture, " part du client ", trajet[0], " et retourne au dépot", "\n")
                text += "La voiture " + str (numVoiture) + " part du client " + str (trajet[0]) + " et retourne au dépot" + "\n"
            elif trajet[0] == 0:
                print("La voiture ", numVoiture, " commence son trajet du dépot et va au client ", trajet[1])
                text += "La voiture " + str (numVoiture) + " commence son trajet du dépot et va au client " + str (trajet[1]) + "\n"
            else:
                print("La voiture ", numVoiture, " va du client ", trajet[0]," au client ",trajet[1])
                text += "La voiture " + str (numVoiture) + " va du client " + str (trajet[0]) + " au client " + str (trajet[1]) + "\n"
            tableau_trie.remove(trajet)
            text += trouver_trajets(trajet[1], tableau_trie, numVoiture)
            break
    return text

# Fonction pour afficher les trajets dans la console
def affichageConsole(trajets):

    # Triez les trajets en fonction du numéro du véhicule
    trajets_tries = sorted(trajets, key=lambda x: int(x[2]))

    # Dictionnaire pour stocker les trajets par véhicule
    trajets_par_vehicule = {}

    # Remplir le dictionnaire avec les trajets pour chaque véhicule
    for trajet in trajets_tries:
        vehicule = trajet[2]
        if vehicule not in trajets_par_vehicule:
            trajets_par_vehicule[vehicule] = []
        trajets_par_vehicule[vehicule].append(trajet)


    tab_trajet_trie=[]

    # Afficher les trajets pour chaque véhicule
    for vehicule, trajets_vehicule in trajets_par_vehicule.items():
        tabtemp=[]
        for trajet in trajets_vehicule:
            tabtemp.append([trajet[0], trajet[1]])
        tab_trajet_trie.append(tabtemp)

    cpt=1

    text=""
    for trajets in tab_trajet_trie:
        trajets = [[int(element) for element in sublist] for sublist in trajets]
        tableau_trie = sorted(trajets, key=lambda x: int(x[0]))

        # Appel de la fonction pour trouver et afficher les trajets
        text += str (trouver_trajets(0, tableau_trie, cpt)) + "\n"
        cpt+=1
    return text


root = tk.Tk()
root.title("Interface graphique pour VRP")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

lp_files_combobox = ttk.Combobox(frame, state="readonly")
lp_files_combobox.pack(side=tk.LEFT, padx=5)

browse_directory(None)

lp_files_combobox.bind("<<ComboboxSelected>>", browse_directory)

# Bouton pour valider la sélection
validate_button = tk.Button(frame, text="Valider", command=run_selected_lp)
validate_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

print(selected_file)
