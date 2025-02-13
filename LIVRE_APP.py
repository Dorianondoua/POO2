import sqlite3
from abc import ABC, abstractmethod
import customtkinter as ctk

# Classe abstraite Document
class Document(ABC):
    @abstractmethod
    def get_details(self):
        pass

# Classe Livre héritant de Document
class Livre(Document):
    def __init__(self, titre, auteur, annee, genre):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre

    def get_details(self):
        return f"{self.titre} par {self.auteur}, {self.annee}, Genre: {self.genre}"

# Classe Bibliotheque pour gérer la collection
class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.conn = sqlite3.connect('bibliotheque.db')
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS livres
                                 (titre TEXT, auteur TEXT, annee INTEGER, genre TEXT)''')

    def ajouter_livre(self, livre):
        self.livres.append(livre)
        with self.conn:
            self.conn.execute("INSERT INTO livres VALUES (?, ?, ?, ?)",
                              (livre.titre, livre.auteur, livre.annee, livre.genre))

    def supprimer_livre(self, titre):
        self.livres = [livre for livre in self.livres if livre.titre != titre]
        with self.conn:
            self.conn.execute("DELETE FROM livres WHERE titre = ?", (titre,))

    def rechercher(self, titre=None, auteur=None):
        resultats = []
        for livre in self.livres:
            if (titre and titre in livre.titre) or (auteur and auteur in livre.auteur):
                resultats.append(livre)
        return resultats

    def afficher_liste(self):
        return [livre.get_details() for livre in self.livres]

# Interface graphique
class App:
    def __init__(self, root):
        self.bibliotheque = Bibliotheque()
        self.root = root
        self.root.title("Gestion de Bibliothèque")
        self.root.geometry("1280x720")

        self.tabview = ctk.CTkTabview(master=root, width=1300, height=650)
        self.tabview.place(x=0, y=0)

        self.tabview.add("info")
        self.tabview.add("affichage")

        self.titre_label=ctk.CTkLabel(root, text="Entrez le titre :", font=("Century Gothic",14) , text_color="green")
        self.titre_label.place(x=30, y=160)
        self.titre_entry = ctk.CTkEntry(root, placeholder_text="Titre")
        self.titre_entry.place(x=30, y=200)

        self.auteur_label= ctk.CTkLabel(root,text="Entrez l'auteur :", font=("Century Gothic", 14),text_color="green")
        self.auteur_label.place(x=210, y=160)
        self.auteur_entry = ctk.CTkEntry(root, placeholder_text="Auteur")
        self.auteur_entry.place(x=210, y=200)

        self.annee_label=ctk.CTkLabel(root, text="Entrez l'année :", font=("Century Gothic", 14),text_color="green" )
        self.annee_label.place(x=380, y=160)
        self.annee_entry = ctk.CTkEntry(root, placeholder_text="Année")
        self.annee_entry.place(x=380, y=200)

        self.genre_label=ctk.CTkLabel(root, text="Entrez la genre :", font=("Century Gothic", 14), text_color="green" )
        self.genre_label.place(x=530, y=160)
        self.genre_entry = ctk.CTkEntry(root, placeholder_text="Genre")
        self.genre_entry.place(x=530, y=200)

        self.ajouter_button = ctk.CTkButton(root, text="Ajouter Livre", border_color="green", font=('Century Gothic', 15),
                       border_width=2,
                      width=200, corner_radius=12, text_color='green', fg_color='white',command=self.ajouter_livre)
        self.ajouter_button.place(x=100, y=340)

        self.supprimer_button = ctk.CTkButton(root, text="Supprimer Livre", border_color="green", font=('Century Gothic', 15),
                       border_width=2,
                      width=200, corner_radius=12, text_color='green', fg_color='white', command=self.supprimer_livre)
        self.supprimer_button.place(x=320, y=340)

        self.rechercher_button = ctk.CTkButton(root, border_color="green", font=('Century Gothic', 15),
                       border_width=2,
                      width=200, corner_radius=12, text_color='green', fg_color='white', text="Rechercher", command=self.rechercher_livre)
        self.rechercher_button.place(x=160, y=420)

        self.afficher_button = ctk.CTkButton(root, text="Afficher Liste", border_color="green", font=('Century Gothic', 15),
                       border_width=2,
                      width=200, corner_radius=12, text_color='green', fg_color='white', command=self.afficher_liste)
        self.afficher_button.place(x=800,y=600)



        self.resultat_label = ctk.CTkLabel(root, width=450, fg_color='white', height=500,
                                     corner_radius=6,text="")
        self.resultat_label.place(x=700, y=80)

    def ajouter_livre(self):
        try:
            titre = self.titre_entry.get()
            auteur = self.auteur_entry.get()
            annee = int(self.annee_entry.get())
            genre = self.genre_entry.get()
            livre = Livre(titre, auteur, annee, genre)
            self.bibliotheque.ajouter_livre(livre)
            self.resultat_label.configure(text="Livre ajouté avec succès.")
        except Exception as e:
            self.resultat_label.configure(text=f"Erreur: {str(e)}")

    def supprimer_livre(self):
        try:
            titre = self.titre_entry.get()
            self.bibliotheque.supprimer_livre(titre)
            self.resultat_label.configure(text="Livre supprimé avec succès.")
        except Exception as e:
            self.resultat_label.configure(text=f"Erreur: {str(e)}")

    def rechercher_livre(self):
        try:
            titre = self.titre_entry.get()
            auteur = self.auteur_entry.get()
            resultats = self.bibliotheque.rechercher(titre, auteur)
            self.resultat_label.configure(text="\n".join([livre.get_details() for livre in resultats]))
        except Exception as e:
            self.resultat_label.configure(text=f"Erreur: {str(e)}")

    def afficher_liste(self):
        try:
            livres = self.bibliotheque.afficher_liste()
            self.resultat_label.configure(text="\n".join(livres))
        except Exception as e:
            self.resultat_label.configure(text=f"Erreur: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()