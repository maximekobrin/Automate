import os
def choisir_fichier():
    dossier = "/Users/maximekobrin/Documents/Python PS/GitHub/Untitled/txt"  # Dossier où se trouvent tes fichiers
    fichiers = [f for f in os.listdir(dossier) if f.endswith('.txt')]  # Liste des fichiers .txt

    if not fichiers:
        print("Aucun fichier disponible.")
        return None

    while True:
        choix = input("Entrez le numéro du fichier que vous voulez utiliser : ")
        if choix.isdigit() and 1 <= int(choix) <= len(fichiers):
            return os.path.join(dossier, fichiers[int(choix) - 1])
        print("Choix invalide, veuillez entrer un numéro valide.")

class AutomateFini:
    def __init__(self, chemin_fichier):
        # Ouvrir le fichier en mode lecture et lire la première ligne
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            premiere_ligne = fichier.readline().strip()  # Lit la première ligne et enlève les espaces ou retours à la ligne
            deuxième_ligne = fichier.readline().strip()
            troisième_ligne = fichier.readline().strip()
            quatrième_ligne = fichier.readline().strip()
            cinquième_ligne = fichier.readline().strip()
            sixième_ligne = fichier.readline().strip()

        #Nombre de symbole dans l'alphabet
        self.nb_symbole_alphabet = premiere_ligne

        #Nombre d'état
        self.nb_etats = deuxième_ligne

        #nombre d’états initiaux
        self.nb_etat_initiaux = troisième_ligne


        # Vous pouvez également affecter cette valeur à d'autres attributs si besoin
        self.etats_initial = troisième_ligne
        self.etats_finaux = quatrième_ligne

        self.nb_transition = cinquième_ligne
        # Initialisation des transitions (ici, vide par défaut)
        self.transitions = sixième_ligne

    def accepte(self, chaine):
        etat_actuel = self.etats_initial
        for symbole in chaine:
            if symbole in self.transitions[etat_actuel]:
                etat_actuel = self.transitions[etat_actuel][symbole]
            else:
                return False
        return etat_actuel in self.etats_finaux


# Exemple d'utilisation :
chemin_selectionne = choisir_fichier()
if chemin_selectionne:
    automate = AutomateFini(chemin_selectionne)
    print("nombre de symboles dans l’alphabet de l’automate : ", automate.nb_symbole_alphabet)
    print("nombre d’états : ", automate.nb_etats)
    print("nombre d’états initiaux, suivi de leurs numéros : ", automate.nb_etat_initiaux)
    print("nombre d’états terminaux, suivi de leurs numéros : ", automate.nb_etat_initiaux)
    print("nombre de transitions : ", automate.nb_transition)
    print("transitions : ", automate.sixième_ligne)

automate = AutomateFini()
print(accepte(automate,"bbaaa")) # True
print(accepte(automate,"a")) # False