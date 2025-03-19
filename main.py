import os
from collections import defaultdict
def choisir_fichier():
    dossier = "/Users/maximekobrin/Documents/Python PS/GitHub/Untitled/txt"  # Dossier où se trouvent tes fichiers
    fichiers = [f for f in os.listdir(dossier) if f.endswith('.txt')]  # Liste des fichiers .txt

    if not fichiers:
        print("Aucun fichier disponible.")
        return None

    fichiers.sort(key=lambda x: int(x.split('.')[0]))  # Trier les fichiers numériquement

    print("Fichiers disponibles :")
    for i, fichier in enumerate(fichiers):
        print(f"{i + 1}. {fichier}")  # Afficher les fichiers avec un numéro

    while True:
        choix = input("Entrez le numéro du fichier que vous voulez utiliser : ")
        if choix.isdigit() and 1 <= int(choix) <= len(fichiers):
            return os.path.join(dossier, fichiers[int(choix) - 1])
        print("Choix invalide, veuillez entrer un numéro valide.")

class AutomateFini:
    def __init__(self, chemin_fichier):
        # Ouvrir le fichier en mode lecture et lire la première ligne
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            lignes = [ligne.strip() for ligne in fichier.readlines()]

        #Nombre de symbole dans l'alphabet
        self.nombre_symboles = int(lignes[0])

        #Nombre d'état
        self.nombre_etats = int(lignes[1])

        #états initiaux
        self.etats_initiaux_data = lignes[2].split()
        self.nombre_etats_initiaux = int(self.etats_initiaux_data[0])
        self.etats_initiaux = set(self.etats_initiaux_data[1:])

        #Etat finaux
        self.etats_finaux_data = lignes[3].split()
        self.nombre_etats_finaux = int(self.etats_finaux_data[0])
        self.etats_finaux = set(self.etats_finaux_data[1:])

        print(lignes)
        #Transition
        self.nombre_transitions = int(lignes[4])
        self.transitions = {}
        for i in range(5, 5 + self.nombre_transitions):  # Parcours des lignes de transition
            elements = lignes[i].split()
            etat_depart = elements[0]
            symboles = elements[1].split(',')  # Symboles séparés par des virgules
            etat_arrivee = elements[2]

            for symbole in symboles:
                self.transitions.setdefault((etat_depart, symbole), set()).add(etat_arrivee)

    def accepte(self, chaine):

        etats_actuels = self.etats_initiaux  # On commence avec les états initiaux

        for symbole in chaine:
            nouveaux_etats = set()
            for etat in etats_actuels:
                if (etat, symbole) in self.transitions:
                    nouveaux_etats.update(self.transitions[(etat, symbole)])

            if not nouveaux_etats:  # Si aucun nouvel état n'est atteint, la chaîne est rejetée
                return False
            etats_actuels = nouveaux_etats  # Mise à jour des états courants

        # Vérifie si au moins un des états actuels est un état final
        return any(etat in self.etats_finaux for etat in etats_actuels)

    #déterminisation de l'automate
        #si : - 1 seul état initial, - chaque état possède au max 1 transition par symbole, - aucune transition ε
    def est_deterministe(self):
        if len(self.etats_initiaux) > 1:
            return False, "l'automate n'est pas une automate déterministe, plusieurs états initiaux" # pLus d'un état
        for (etat,symbole), destinations in self.transitions.items():
            if len(destinations) > 1:
                return False, "l'automate n'est pas une automate déterministe, plusieurs à partir du même état du même symbole"
            if symbole == "ε":
                return False, "l'automate n'est pas une automate déterministe, il existe une ou plusieurs ε-transition"

        return True, "l'automate est déterministe"






# 🔹 Sélection du fichier
chemin_selectionne = choisir_fichier()
if chemin_selectionne:
    automate = AutomateFini(chemin_selectionne)

    # 🔹 Affichage des informations de l'automate
    print("\n🔹 Informations de l'Automate 🔹")
    print("Nombre de symboles :", automate.nombre_symboles)
    print("Nombre d'états :", automate.nombre_etats)
    print("États initiaux :", automate.etats_initiaux)
    print("États finaux :", automate.etats_finaux)
    print("Nombre de transitions :", automate.nombre_transitions)
    print("Transitions :")
    for (etat, symbole), destinations in automate.transitions.items():
        print(f"  {etat} --({symbole})--> {destinations}")

    # 🔹 Tester si des chaînes sont acceptées
    print("\n🔹 Tests d'acceptation 🔹")
    print(f"Chaîne 'a' : {automate.accepte('a')}")
    print(f"Chaîne 'bbaaa' : {automate.accepte('bbaaa')}")

#Déterministe ou non
is_deterministic, message = automate.est_deterministe()
print(message)

