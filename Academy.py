import customtkinter as ct
import pandas as pa

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
    valeur = input("Tu veux une interfaces graphique ? (Yes/No) \n")
    if valeur == "Yes" or valeur == "Y" or valeur == "y" or valeur == "yes":
        return Accept()
    return Refuse()

def button_callback(): # Fonction de test
    print("button clicked")

def Accept(): # Affichage d'une fenetre
    app = ct.CTk()
    app.geometry("500x400")

    textbox = ct.CTkTextbox(app, width=400, height=200)
    textbox.pack(pady=20)

    button = ct.CTkButton(app, text="my button", command=button_callback) # Quand on click elle appel la fonction button_callback()
    button.pack(padx=20, pady=20)

    app.mainloop()

def Refuse():
    reponce = Reponce() # On demande a l'utilisateur de saisir les données et on appel la fonction Reponce()
    taux_reussite = pa.read_csv("./fr-en-indicateurs-valeur-ajoutee-colleges.csv", delimiter=";") # On attribue les données des resultat par etablisement a une variable
    localisation_etablisement = pa.read_csv("./ips-all-geoloc.csv", delimiter=";") # On attribue les données des localisation des etablisement a une variable
    for i in range(0,len(reponce),2):
        print(taux_reussite)
    print(reponce)

def Reponce():
    request = input("Que voulez vous savoir ? (Exemple: UAI: 0382426F, Département: AIN) \n")
    pairs = request.split(", ")  # On separe les paires
    result = []
    for pair in pairs:
        key_value = pair.split(": ")  # On separe les cles et les valeurs
        result.extend(key_value)  # On ajoute les cles et les valeurs à la liste
    print(result)
    return result
print(main())