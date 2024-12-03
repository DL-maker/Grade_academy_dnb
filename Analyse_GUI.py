import os
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import logging
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Analyseur de Données CSV")
        master.geometry("600x400")
        
        # Style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 10))

        # Variables
        self.repertoire = tk.StringVar(value=os.getcwd())
        self.fichiers_csv = []
        self.connection_base = None

        # Configuration du logging
        self.configurer_logging()

        # Créer les widgets
        self.creer_widgets()

    def configurer_logging(self):
        """Configure la journalisation"""
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'analyse_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def creer_widgets(self):
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

        # Bouton de lancement de l'analyse
        btn_analyser = ttk.Button(main_frame, text="Lancer l'Analyse", command=self.lancer_analyse)
        btn_analyser.pack(pady=10)

        

        # Frame pour les requêtes SQL
        sql_frame = ttk.Frame(main_frame)
        sql_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(sql_frame, text="Requête SQL :").pack(side=tk.LEFT)
        self.entry_requete_sql = ttk.Entry(sql_frame, width=60)
        self.entry_requete_sql.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        btn_executer_sql = ttk.Button(sql_frame, text="Exécuter SQL", command=self.executer_requete_sql)
        btn_executer_sql.pack(side=tk.LEFT)


        # Notebook pour les résultats
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
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
            
            dataframes = {}
            for fichier in self.fichiers_csv:
                chemin_complet = os.path.join(repertoire, fichier)
                nom_table = os.path.splitext(fichier)[0]
                
                try:
                    df = pd.read_csv(chemin_complet, low_memory=False, on_bad_lines='skip')
                    df.to_sql(nom_table, self.connection_base, if_exists='replace', index=False)
                    dataframes[nom_table] = df
                    self.logger.info(f"Chargement de {fichier} réussi")
                except Exception as e:
                    self.logger.error(f"Erreur lors du chargement de {fichier}: {e}")
            
            return dataframes
        except Exception as e:
            self.logger.error(f"Erreur de chargement des données : {e}")
            return None

    def executer_requete_sql(self):
        """Exécute une requête SQL et affiche les résultats"""
        if not self.connection_base:
            messagebox.showwarning("Attention", "Aucune base de données chargée.")
            return

        requete_sql = self.entry_requete_sql.get().strip()
        if not requete_sql:
            messagebox.showwarning("Attention", "Veuillez saisir une requête SQL.")
            return

        try:
            # Créer un nouvel onglet pour les résultats SQL
            frame_sql = ttk.Frame(self.notebook)
            self.notebook.add(frame_sql, text="Résultats SQL")

            # Zone de texte scrollable pour les résultats
            resultats_text = scrolledtext.ScrolledText(frame_sql, wrap=tk.WORD)
            resultats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Exécuter la requête
            df_resultat = pd.read_sql_query(requete_sql, self.connection_base)
            
            # Afficher les résultats
            resultats_text.insert(tk.END, str(df_resultat))
            
            # Sélectionner le nouvel onglet
            self.notebook.select(frame_sql)

            self.logger.info(f"Requête SQL exécutée : {requete_sql}")

        except Exception as e:
            messagebox.showerror("Erreur SQL", str(e))
            self.logger.error(f"Erreur lors de l'exécution de la requête SQL : {e}")

    def generer_visualisations(self, dataframes):
        """Génère des visualisations pour les dataframes chargés"""
        for nom_table, df in dataframes.items():
            # Créer un nouvel onglet pour chaque dataframe
            frame_analyse = ttk.Frame(self.notebook)
            self.notebook.add(frame_analyse, text=f"Analyse {nom_table}")

            # Résumé statistique
            resume_frame = ttk.Frame(frame_analyse)
            resume_frame.pack(fill=tk.X, padx=10, pady=10)
            
            resume_text = scrolledtext.ScrolledText(resume_frame, height=10, width=80)
            resume_text.pack()
            resume_text.insert(tk.END, f"Résumé statistique pour {nom_table}:\n\n")
            resume_text.insert(tk.END, str(df.describe()))

            # Graphiques de base
            graphiques_frame = ttk.Frame(frame_analyse)
            graphiques_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Sélection des colonnes numériques
            colonnes_numeriques = df.select_dtypes(include=['int64', 'float64']).columns

            if len(colonnes_numeriques) > 0:
                # Histogramme de la première colonne numérique
                fig, ax = plt.subplots(figsize=(8, 4))
                df[colonnes_numeriques[0]].hist(ax=ax)
                ax.set_title(f'Histogramme de {colonnes_numeriques[0]}')
                
                canvas = FigureCanvasTkAgg(fig, master=graphiques_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()

    def lancer_analyse(self):
        """Exécute l'ensemble du processus d'analyse"""
        try:
            # Réinitialiser le notebook
            for i in self.notebook.winfo_children():
                i.destroy()

            # Lister les fichiers CSV
            fichiers = self.lister_fichiers_csv()
            
            if not fichiers:
                messagebox.showwarning("Attention", "Aucun fichier CSV trouvé dans le répertoire.")
                return

            # Charger dans SQLite et obtenir les dataframes
            dataframes = self.charger_donnees_sqlite()
            if not dataframes:
                messagebox.showerror("Erreur", "Échec du chargement des données")
                return
            
            # Générer des visualisations
            self.generer_visualisations(dataframes)
            
            self.notebook.select(self.notebook.winfo_children()[0])
            messagebox.showinfo("Analyse Terminée", "L'analyse des données est complète.")
        
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            self.logger.error(f"Erreur lors de l'analyse : {e}")

def main():
    root = tk.Tk()
    app = DataAnalysisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()