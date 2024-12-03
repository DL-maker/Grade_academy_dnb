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
    parser.add_argument( "--no-gui", help="Voulez vous une interfqce grqphique ?", action="store_true") # On ajoute un argument pour le fichier CSV
    args = parser.parse_args() # On parse les arguments
    if args.no_gui: # Si l'argument est present on lance le mode CLI
        return cli() 
    return main_gui()


def cli():
    reponce = input("Que voulez vous avoir ?").split(": ")
    taux_reussite = pd.read_csv("./fr-en-indicateurs-valeur-ajoutee-colleges.csv", delimiter=";") # On attribue les données des resultat par etablisement a une variable
    localisation_etablisement = pd.read_csv("./ips-all-geoloc.csv", delimiter=";") # On attribue les données des localisation des etablisement a une variable
    resultat = taux_reussite[taux_reussite[reponce[0]] == reponce[1]] # On cherche les données
    print(reponce)
    print(resultat)


if __name__ == "__main__":
    main()