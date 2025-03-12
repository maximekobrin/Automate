def lire_ligne_fichier(chemin_fichier, numero_ligne):
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            lignes = fichier.readlines()  # Lire toutes les lignes dans une liste
            if 1 <= numero_ligne <= len(lignes):  # Vérifier si la ligne existe
                return lignes[numero_ligne - 1].strip()  # Retourne la ligne sans les espaces inutiles
            else:
                return f"La ligne {numero_ligne} n'existe pas dans le fichier."
    except FileNotFoundError:
        return "Fichier introuvable."
    except Exception as e:
        return f"Une erreur est survenue : {e}"



class AutomateFini:
    def __init__(self, chemin_fichier):
        # Ouvrir le fichier en mode lecture et lire la première ligne
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            premiere_ligne = fichier.readline().strip()  # Lit la première ligne et enlève les espaces ou retours à la ligne
            deuxième_ligne = fichier.readline().strip()
            troisième_ligne = fichier.readline().strip()

        # Affecter la valeur lue à self.etats
        self.etats = premiere_ligne

        # Vous pouvez également affecter cette valeur à d'autres attributs si besoin
        self.etat_initial = deuxième_ligne
        self.etats_finaux = troisième_ligne

        # Initialisation des transitions (ici, vide par défaut)
        self.transitions = {}

    def accepte(self, chaine):
        etat_actuel = self.etat_initial
        for symbole in chaine:
            if symbole in self.transitions[etat_actuel]:
                etat_actuel = self.transitions[etat_actuel][symbole]
            else:
                return False
        return etat_actuel in self.etats_finaux


# Exemple d'utilisation
chemin = "/Users/maximekobrin/Documents/Python PS/GitHub/Untitled/txt/1.txt"  # Remplace par le chemin réel de ton fichier
ligne_voulue = 1  # Par exemple, lire la 1e ligne
print(lire_ligne_fichier(chemin, ligne_voulue))