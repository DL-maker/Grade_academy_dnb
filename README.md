# GrandAnalyser - Outil Complet d'Analyse de Données CSV

## 🚀 Description du Projet

GrandAnalyser est une application Python permettant l'analyse de fichiers CSV avec une interface graphique (GUI) et une option de ligne de commande. Développé par Laith & Adel, cet outil offre une flexibilité maximale pour l'exploration et l'analyse de données.

## ✨ Fonctionnalités Principales

### Interface Graphique (GUI)
- Chargement de fichiers CSV depuis un répertoire
- Analyse statistique des données
- Visualisation graphique des données
- Exécution de requêtes SQL interactives
- Journalisation détaillée des opérations

### Mode Ligne de Commande
- Recherche flexible dans les datasets
- Filtrage des données par colonnes et valeurs
- Support des arguments de ligne de commande

## 🛠️ Prérequis Techniques

### Dépendances
- Python 3.8+
- Bibliothèques requises :
  - pandas
  - sqlite3
  - tkinter
  - matplotlib
  - logging

### Installation

1. Cloner le dépôt
```bash
git clone https://github.com/DL-maker/Grade_academy_dnb.git
cd GrandAnalyser
```

2. Installer les dépendances
```bash
pip install pandas matplotlib
```

## 🖥️ Utilisation

### Lancement de l'Interface Graphique
```bash
python Analyse_GUI.py
```

### Utilisation en Ligne de Commande
```bash
# Lancement sans GUI
python Academy.py --no-gui

# Recherche spécifique
python Academy.py --recherche "colonne1: valeur1, colonne2: valeur2"
```

## 📝 Options de Ligne de Commande

- `--no-gui`: Désactive l'interface graphique
- `--no-question`: Désactive les invites de saisie interactive
- `--recherche`: Permet une recherche personnalisée dans les données

## 🗂️ Structure des Fichiers

- `Analyse_GUI.py`: Interface graphique principale
- `Academy.py`: Point d'entrée du programme
- `*.csv`: Fichiers de données source

## 🔍 Exemple de Recherche

```
Que voulez-vous avoir ? académie: Lyon, Specifiques: nom_etablissement
```

## 🚧 Gestion des Erreurs

L'application inclut une gestion robuste des erreurs avec :
- Journalisation détaillée
- Messages d'erreur explicites
- Gestion des fichiers CSV mal formatés

## 📃License
Protected by an MIT license

## 👥 Auteurs

- Laith
- Adel
