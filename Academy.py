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
    taux_reussite = pd.read_csv("./fr-en-indicateurs-valeur-ajoutee-colleges.csv", delimiter=";") # On attribue les données des resultat par etablisement a une variable
    localisation_etablisement = pd.read_csv("./ips-all-geoloc.csv", delimiter=";") # On attribue les données des localisation des etablisement a une variable
    taux_reussite_2008 = pd.read_csv("./fr-en-dnb-par-etablissement.csv", delimiter=";") # On attribue les données des resultat par etablisement a une variable pour 2008 
    # On ajoute les colonnes des données dans un dictionnaire
    Columns['taux_reussite'] = list(taux_reussite.colonnes)
    Columns['localisation_etablisement'] = list(localisation_etablisement.colonnes)
    Columns['taux_reussite_2008'] = list(taux_reussite_2008.colonnes)

    reponce = input("Que voulez vous avoir ? \n").split(": ")

    if not reponce or len(reponce) < 2:  # On check si l'utilisateur a bien entré les arguments
        print("Veuillez entrer un argument valide sous la forme 'colonne: valeur'")
        return
    
    titre_colums = [] # On crée une liste pour check dans quelle colonne est demande

    if reponce[0] in Columns['taux_reussite']:
        titre_colums.append(taux_reussite)
    if reponce[0] in Columns['localisation_etablisement']:
        titre_colums.append(localisation_etablisement)
    if reponce[0] in Columns['taux_reussite_2008']:
        titre_colums.append(taux_reussite_2008)
    if not titre_colums:
        print("Colonne non trouvée")
        return
    
    if len(reponce[0]) + len(reponce[1]) < 5: # On check si l'utilisateur a bien entré les arguments
        print("Veuillez entrer un argument valide sous la forme 'colonne: valeur'")
        return
    
    if reponce[0] not in taux_reussite.colonnes: # On check si la colonne n'est pas dans le fichier
        print(f"Colonne '{reponce[0]}' non trouvée") # Si oui on affiche un message d'erreur
        return
    
    meme_colonnes = set(Columns['taux_reussite']).intersection(Columns['localisation_etablisement'], Columns['taux_reussite_2008']) # On check les colonnes communes
    print(f"Colonnes equivalent: {meme_colonnes}") # On affiche les colonnes communes
    resultat = []

    for df in titre_colums:
        envoie = df[list(meme_colonnes)] # On crée un envoie avec les colonnes communes pour chaque dataframe dans titre_colums
        resultat.append(envoie) # On ajoute le envoie a la liste resultat
    resultat = pd.concat(resultat) # On conscate les resultats
    print(resultat) # On affiche les resultats (affiche que des index :'(  )


if __name__ == "__main__":
    main()