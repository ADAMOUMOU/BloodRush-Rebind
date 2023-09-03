import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import simpledialog
import webbrowser


# Fonction pour ouvrir un fichier de configuration
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers INI", "*.ini")])
    if file_path:
        load_configuration(file_path)


# Fonction pour charger et afficher les données du fichier
def load_configuration(file_path):
    tree.delete(*tree.get_children())
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("+ActionMappings"):
                parts = line.split(",")

                # Trouver l'index du début de "ActionName="
                index_action_name = parts[0].find('ActionName=')

                # Trouver l'index de la première guillemet après "ActionName="
                index_debut_nom = parts[0].find('"', index_action_name)

                # Trouve l'index de la deuxième guillemet après "ActionName="
                index_fin_nom = parts[0].find('"', index_debut_nom + 1)

                # Extrais la sous-chaîne entre les deux guillemets
                action_name = parts[0][index_debut_nom + 1:index_fin_nom]

                key = parts[-1].split("=")[1].strip().strip('"').translate(str.maketrans('', '', ")"))
                tree.insert("", "end", values=(action_name, key))


# Fonction pour modifier la touche associée à une action
def modify_key(event):
    item = tree.selection()[0]
    action_name = tree.item(item, "values")[0]
    current_key = tree.item(item, "values")[1]

    new_key = simpledialog.askstring("Modifier la touche", f"Modifier la touche pour {action_name}",
                                     initialvalue=current_key)

    if new_key:
        tree.item(item, values=(action_name, new_key))


# Fonction pour sauvegarder les changements
def save_changes():
    file_path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("Fichiers INI", "*.ini")])
    if file_path:
        with open(file_path, "w") as file:
            for item in tree.get_children():
                action_name, key = tree.item(item, "values")
                file.write(
                    f'+ActionMappings=(ActionName="{action_name}",bShift=False,bCtrl=False,bAlt=False,bCmd=False,Key={key})\n')


# Fonction pour ouvrir le site web lorsque le lien est cliqué
def open_website():
    webbrowser.open("https://docs.unrealengine.com/udk/Three/KeyBinds.html#Mappable%20keys")


# Créer la fenêtre principale
root = tk.Tk()
root.title("Assignations de touches")

# Créer un bouton pour ouvrir le fichier de configuration
open_button = ttk.Button(root, text="Ouvrir fichier", command=open_file)

# Créer un tableau pour afficher les données
tree = ttk.Treeview(root, columns=("ActionName", "Key"), show="headings")
tree.heading("ActionName", text="ActionName")
tree.heading("Key", text="Key")

open_file()

# Activer la modification de la touche par double-clic
tree.bind("<Double-1>", modify_key)

# Créer un bouton pour sauvegarder les modifications
save_button = ttk.Button(root, text="Sauvegarder les modifications", command=save_changes)

# Placer les éléments dans la fenêtre
open_button.pack(padx=10, pady=10)
tree.pack(padx=10, pady=10)
save_button.pack()

# Créer un label cliquable pour ouvrir le site
website_label = tk.Label(root, text="Documentation", fg="blue", cursor="hand2")
website_label.pack()
website_label.bind("<Button-1>", lambda event: open_website())

root.mainloop()
