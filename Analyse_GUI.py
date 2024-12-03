import os
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class DataAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Analyseur de Données CSV")
        master.geometry("500x150")
        
        # Style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 10))

        # Variables
        self.repertoire = tk.StringVar(value=os.getcwd())
        self.fichiers_csv = []
        self.connection_base = None

        # Créer les widgets
        self.creer_widgets()


    def creer_widgets(self): # Créer les widgets de l'interface graphique
        # Frame principale
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sélection du répertoire
        repertoire_frame = ttk.Frame(main_frame)
        repertoire_frame.pack(fill=tk.X, pady=10)

        ttk.Label(repertoire_frame, text="Répertoire :").pack(side=tk.LEFT)
        entry_repertoire = ttk.Entry(repertoire_frame, textvariable=self.repertoire, width=50)
        entry_repertoire.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        btn_parcourir = ttk.Button(repertoire_frame, text="Parcourir", command=self.choisir_repertoire)
        btn_parcourir.pack(side=tk.LEFT)

    def choisir_repertoire(self):
        """Ouvre un dialogue pour choisir le répertoire"""
        repertoire_choisi = filedialog.askdirectory()
        if repertoire_choisi:
            self.repertoire.set(repertoire_choisi)

    def lister_fichiers_csv(self):
        """Liste tous les fichiers CSV du répertoire"""
        repertoire = self.repertoire.get()
        self.fichiers_csv = [
            f for f in os.listdir(repertoire) 
            if f.endswith('.csv')
        ]
        self.logger.info(f"Fichiers CSV trouvés : {self.fichiers_csv}")
        return self.fichiers_csv

    def charger_donnees_sqlite(self):
        """Charge les fichiers CSV dans une base SQLite en mémoire"""
        try:
            repertoire = self.repertoire.get()
            self.connection_base = sqlite3.connect(':memory:')
            
            for fichier in self.fichiers_csv:
                chemin_complet = os.path.join(repertoire, fichier)
                nom_table = os.path.splitext(fichier)[0]
                
                try:
                    df = pd.read_csv(chemin_complet, low_memory=False, on_bad_lines='skip')
                    df.to_sql(nom_table, self.connection_base, if_exists='replace', index=False)
                    self.logger.info(f"Chargement de {fichier} réussi")
                except Exception as e:
                    self.logger.error(f"Erreur lors du chargement de {fichier}: {e}")
            
            return True
        except Exception as e:
            self.logger.error(f"Erreur de chargement des données : {e}")
            return False

def main_gui():
    root = tk.Tk()
    app = DataAnalysisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main_gui()