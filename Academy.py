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

    columns = recharge_des_bd()
        
    # Récupération de l'input utilisateur
    reponce = input_user()

    # Vérification de l'input
    if not reponce or len(reponce) < 2:
        print("Veuillez entrer un argument valide sous la forme 'colonne: valeur'")
        return
            
    # Recherche des colonnes et affichage
    colonnes_trouvees = rechercher_colonne(reponce)
    valeur_trouvees = rechercher_valeur(reponce)
    print("Colonnes trouvées:", colonnes_trouvees) # C bon
    print("Valeur a trouvees:", valeur_trouvees)
    lien = tableaux_liees(columns, colonnes_trouvees)
    affiche = select(reponce) 
    print(lien) # C bon
    print(affiche) 
    print(affichage(lien, colonnes_trouvees, valeur_trouvees, affiche))

def select(donner): 
    print("Debug select - Donner:", donner)
    for item in donner:
        print("Debug select - Item:", item)
        if item[0] == "Specifiques":
            return item[1].strip()
    return None

def affichage(lien, colonnes_trouvees, valeur_trouvees, affiche):
    result = []
    fichiers = {
        'taux_reussite': './fr-en-indicateurs-valeur-ajoutee-colleges.csv',
        'taux_reussite_2008': './fr-en-dnb-par-etablissement.csv',
        'localisation_etablisement': './ips-all-geoloc.csv'
    }
    
    for table in lien:
        try:
            # Charger le fichier CSV
            df = pd.read_csv(fichiers[table], delimiter=";")
        except Exception as e:
            print(f"Erreur de lecture du fichier {fichiers[table]} : {e}")
            continue

        # Filtrage des lignes sur la base des colonnes et valeurs trouvées
        filtered_df = df.copy()
        for col, val in zip(colonnes_trouvees, valeur_trouvees):
            if col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col].astype(str) == str(val)]
            else:
                print(f"Colonne '{col}' introuvable dans {table}. Colonnes disponibles : {list(filtered_df.columns)}")

        # selectionne la colonne spécifique demandée
        if not filtered_df.empty:
            if affiche:  # gestion des cas "Specifiques"
                if affiche in filtered_df.columns:
                    filtered_df = filtered_df[[affiche]]
                else:
                    print(f"La colonne '{affiche}' demandée n'existe pas dans {table}.")
            result.append(filtered_df)

    # Combine les résultats des différents fichiers
    return pd.concat(result, ignore_index=True).drop_duplicates() if result else pd.DataFrame()




# charger les differents colonnes pour mettre a jour
def recharge_des_bd():
    check_out = {}
    taux_reussite = pd.read_csv("./fr-en-indicateurs-valeur-ajoutee-colleges.csv", delimiter=";")
    localisation_etablisement = pd.read_csv("./ips-all-geoloc.csv", delimiter=";")
    taux_reussite_2008 = pd.read_csv("./fr-en-dnb-par-etablissement.csv", delimiter=";")
    check_out["taux_reussite"] = list(taux_reussite.columns)
    check_out["localisation_etablisement"] = list(localisation_etablisement.columns)
    check_out["taux_reussite_2008"] = list(taux_reussite_2008.columns)
    return check_out

# Fonction pour prendre en compte afficher un colonnes 
def select(donner):
    for item in donner:
        if item[0] == "Specifiques":
            return item[1]
    return None

def rechercher_colonne(valeurs): # Fonction pour rechercher les colonnes
    colonnes = []
    for i in range(len(valeurs)):
        if valeurs[i] != "Specifiques" :
            colonnes.append(valeurs[i][0])
    return colonnes

def rechercher_valeur(valeurs): # Fonction pour rechercher le valeur qui seront en commien 
    colonnes = []
    for i in range(len(valeurs)):
        if valeurs[i] != "Specifiques" :
            colonnes.append(valeurs[i][1])
    return colonnes

# Fonction pour rechercher les tableaux en lien avec les colonnes
def tableaux_liees(columns, colonnes_trouvees):
    Liste = []
    for trouve in colonnes_trouvees:
        for key, valeurs in columns.items():
            if key != "Specifiques":
                if trouve in valeurs and key not in Liste:
                    Liste.append(key)
    return Liste

# Fonction pour l'input utilisateur
def input_user():
    reponce = input("Que voulez-vous avoir ? \n").split(", ")
    reponce = [i.split(": ") for i in reponce]
    return [[item[0], item[1]] for item in reponce if len(item) == 2] # On retourne une liste de liste pour but de faciliter la recherche des colonnes et valeurs


if __name__ == "__main__":
    main()