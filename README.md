Projet VRP
==================
# Presentation

Ce projet a été réalisé dans le cadre de la troisième année du BUT Informatique. Il s’inscrit dans une démarche de résolution algorithmique et d’optimisation, appliquée au **Vehicle Routing Problem (VRP)** – un problème d’optimisation combinatoire consistant à planifier les tournées d’une flotte de véhicules pour livrer une liste de clients tout en minimisant les coûts.

Le principe de l'application est de permettre :
- **Résolution du VRP** : Utiliser IBM CPLEX pour modéliser et résoudre le problème à partir d’un jeu de données.
- **Visualisation des résultats** : Afficher les résultats de la résolution (itinéraires, coût total, etc.) à l’aide d’une interface graphique développée en Python (Tkinter et Matplotlib).

Pour plus de détails sur le modèle mathématique et l’implémentation technique, reportez-vous au [rapport détaillé](https://raw.githubusercontent.com/NoeFBou/ProjetVRPsae601/main/L-Rapport_Projet-Groupe2-SAE6.01.pdf) réalisé par l’équipe.

---

## Installation et Prérequis

Pour utiliser ce projet, assurez-vous de disposer des éléments suivants :

- **Python 3.x**  
  Le projet est développé en Python, avec une interface graphique basée sur Tkinter.

- **IBM CPLEX**  
  Une version (gratuit ou académique) de CPLEX est nécessaire pour résoudre le problème d’optimisation.  
  *Remarque* : La version gratuite de CPLEX peut limiter le nombre de variables, ce qui peut poser problème sur des jeux de données très volumineux (ex. : VRP avec 50 clients).

- **Dépendances Python**  
  Installez les bibliothèques nécessaires, par exemple via `pip` :
  ```bash
  pip install cplex
  ```

---

## Utilisation

### 1. Conversion des Jeux de Données

Avant de résoudre un problème VRP, il est souvent nécessaire de convertir un jeu de données de positions en un format de distances compatible avec CPLEX. Pour cela, exécutez :

```bash
python ConvertirMatrixPositionPourCplex.py
```

Une fenêtre s’ouvre pour vous permettre de sélectionner le fichier source. Le script calcule la matrice de distances et génère un fichier `.dat` qui sera utilisé ultérieurement par CPLEX.

### 2. Résolution et Visualisation du Problème VRP

Lancez l’application principale en exécutant :

```bash
python VRP.py
```

#### Fonctionnalités offertes :

- **Sélection du fichier LP** :  
  Une interface graphique vous permet de choisir parmi les fichiers LP disponibles dans le dossier `./donnees`. Vous pouvez ainsi tester différents jeux de données.

- **Résolution via CPLEX** :  
  Une fois le fichier sélectionné, l’API CPLEX lit et résout le problème. Le programme affiche ensuite dans la console la valeur de la fonction objectif ainsi que les variables non nulles (correspondant aux arcs empruntés par les véhicules).

- **Affichage graphique** :  
  L’interface affiche une carte avec :
  - Un dépôt (représenté par un cercle gris et étiqueté "depot").
  - Les clients (étiquetés "client 1", "client 2", etc.).
  - Les trajets empruntés par les véhicules, représentés par des flèches de couleurs différentes (la couleur est choisie en fonction du véhicule).

- **Affichage textuel** :  
  Le détail des tournées est affiché dans un panneau latéral. Par exemple :

---

## Objectifs Pédagogiques

Les objectifs pédagogiques du projet sont :

- **Modélisation Mathématique** : Élaborer un modèle complet en définissant la fonction objectif et les contraintes.
- **Programmation et Algorithmiques** : Mettre en œuvre l’algorithme de résolution à l’aide de CPLEX et intégrer cette solution dans une application Python.
- **Interface Graphique** : Concevoir une interface graphique pour sélectionner les jeux de données, lancer la résolution et visualiser les itinéraires.
- **Introduction à la recherche et aux concepts mathématiques plus avancés** : Dans le cas de poursuite d'étude en Master.





