import os
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ct
import argparse
from Analyse_GUI import main_gui

def main():
    print(r"""
 _____               _         ___                _                            _       _
|  __ \             | |       / _ \              | |                          | |     | |
| |  \/_ __ __ _  __| | ___  / /_\ \ ___ __ _  __| | ___ _ __ ___  _   _    __| |_ __ | |__
| | __| '__/ _` |/ _` |/ _ \ |  _  |/ __/ _` |/ _` |/ _ \ '_ ` _ \| | | |  / _` | '_ \| '_ \
| |_\ \ | | (_| | (_| |  __/ | | | | (_| (_| | (_| |  __/ | | | | | |_| | | (_| | | | | |_) |
 \____/_|  \__,_|\__,_|\___| \_| |_/\___\__,_|\__,_|\___|_| |_| |_|\__, |  \__,_|_| |_|_.__/
                                                                    __/ |
                                                                   |___/  by Laith & Adel """)
    parser = argparse.ArgumentParser(description="Academy") # On crée un parser pour les arguments
    parser.add_argument( "--no-gui", help="Ne pas activer l'interface graphique", action="store_true") # On ajoute un argument pour le fichier CSV
    args = parser.parse_args() # On parse les arguments
    if args.no_gui: # Si l'argument est present on lance le mode CLI
        return cli() 
    return main_gui()


def cli():

    Columns = {}
    taux_reussite = pd.read_csv("./fr-en-indicateurs-valeur-ajoutee-colleges.csv", delimiter=";")
    localisation_etablisement = pd.read_csv("./ips-all-geoloc.csv", delimiter=";")
    taux_reussite_2008 = pd.read_csv("./fr-en-dnb-par-etablissement.csv", delimiter=";")
        
    # Récupération de l'input utilisateur
    reponce = input("Que voulez vous avoir ? \n").split(": ")

    # Vérification de l'input
    if not reponce or len(reponce) < 2:
        print("Veuillez entrer un argument valide sous la forme 'colonne: valeur'")
        return
            
    # Recherche des colonnes et affichage
    colonnes_trouvees = rechercher_colonne(reponce)
    print("Colonnes trouvées:", colonnes_trouvees)
    print("Arguments reçus:", reponce)


def rechercher_colonne(valeurs):
        colonnes = []
        for i in range(0, len(valeurs), 2):
            if i < len(valeurs):
                colonnes.append(valeurs[i])
        return colonnes


if __name__ == "__main__":
    main()