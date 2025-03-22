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

        #Liste de etats
        self.etats = {etat for (etat, _) in self.transitions.keys()}  # Récupère tous les états
        self.etats.update({e for dest in self.transitions.values() for e in dest})  # Ajoute les états d'arrivée


    #création d'un état qui regroupe l'ensemble des etat accessible uniquement en ε
    def fermeture_epsilon(self, etat):
        fermeture = {etat}  # L'état fait partie de sa propre fermeture ε
        pile = [etat]  # Pile pour explorer les transitions ε

        while pile:
            etat_courant = pile.pop()
            if (etat_courant, "ε") in self.transitions:  # Vérifie si ε-transition existe
                for voisin in self.transitions[(etat_courant, "ε")]:
                    if voisin not in fermeture:
                        fermeture.add(voisin)
                        pile.append(voisin)  # Ajoute le voisin pour continuer l'exploration

        return fermeture

    #elimination des ε-transition
    def eliminer_transitions_epsilon(self):
        nouvelles_transitions = defaultdict(set)

        # 🔹 Calcul de la fermeture ε pour chaque état
        fermeture_epsilon = {etat: self.fermeture_epsilon(etat) for etat in
                             self.etats_initiaux.union(self.etats_finaux)}

        # 🔹 Reconstruction des transitions sans ε
        for (etat, symbole), destinations in self.transitions.items():
            if symbole != "ε":  # On ignore les transitions ε
                for destination in destinations:
                    for etat_f in fermeture_epsilon[etat]:  # Ajouter les fermetures des états sources
                        nouvelles_transitions[(etat_f, symbole)].update(fermeture_epsilon[destination])

        # 🔹 Définition des nouveaux états finaux
        nouveaux_etats_finaux = set()
        for etat, fermeture in fermeture_epsilon.items():
            if any(f in self.etats_finaux for f in fermeture):  # Si un des états de la fermeture est final
                nouveaux_etats_finaux.add(etat)

        # 🔹 Mise à jour de l'automate
        self.transitions = nouvelles_transitions
        self.etats_finaux = nouveaux_etats_finaux
        print("\n✅ Les transitions ε ont été éliminées.")

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

    def is_complet(self):

        # Récupérer tous les symboles utilisés dans l'automate
        alphabet = {s for _, s in self.transitions.keys() if s != "ε"}  # Exclure epsilon

        for etat in self.etats:
            transitions_etat = {s for (_, s) in self.transitions.keys() if _ == etat}  # Symboles disponibles

            # Vérifie si l'état couvre tous les symboles de l'alphabet
            if transitions_etat != alphabet:
                return False, f"Automate non complet : L'état {etat} ne couvre pas tous les symboles ({alphabet - transitions_etat})"

        return True, "L'automate est complet."

    def contient_transition_epsilon(self):
        """Vérifie si l'automate contient au moins une transition ε"""
        return any(symbole == "ε" for _, symbole in self.transitions.keys())


    def is_standard(self):
        if len(self.etats_initiaux) != 1:
            return False

        etat_initial = next(iter(self.etats_initiaux))

        for (etat_depart,symbole), etats_arrivee in self.transitions.items():
            if etat_initial in etats_arrivee and etat_depart != etat_initial:
                return False

        return True

    def standardiser(self):

        if self.is_standard():
            print("L'automate est déjà standard.")
            return self

        nouvel_etat_initial = "état_i"
        #nouveaux_etats = self.etats.union({nouvel_etat_initial})
        #nouvelles_transitions = {**self.transitions}


        self.etats.add(nouvel_etat_initial)


        for etat_initial in self.etats_initiaux:
            self.transitions.setdefault((nouvel_etat_initial, ""), set()).add(etat_initial)


            for (etat_depart, symbole), etats_arrivee in list(self.transitions.items()):
                if etat_depart == etat_initial:
                    self.transitions.setdefault((nouvel_etat_initial, symbole), set()).update(etats_arrivee)

        # Mettre à jour l'état initial
        self.etats_initiaux = {nouvel_etat_initial}

        print("Standardisation terminée.")






    def determiniser(self):
        if self.contient_transition_epsilon():
            self.eliminer_transitions_epsilon()
        else:
            print("pas de relation ε donc direct determinisation")

        nouvel_etat_initial = frozenset(self.etats_initiaux)
        nouveaux_etats = {nouvel_etat_initial}
        nouveaux_etats_a_traiter = [nouvel_etat_initial]
        nouvelles_transitions = {}
        nouveaux_etats_acceptants = set()

        while nouveaux_etats_a_traiter:
            etat_courant = nouveaux_etats_a_traiter.pop()
            nouvelles_transitions[etat_courant] = {}

            for symbole in {s for _, s in self.transitions.keys() if s != "ε"}:
                nouvel_etat = set()
                for etat in etat_courant:
                    if (etat, symbole) in self.transitions:
                        nouvel_etat.update(self.transitions[(etat, symbole)])

                nouvel_etat = frozenset(nouvel_etat)
                if nouvel_etat:
                    nouvelles_transitions[etat_courant][symbole] = nouvel_etat
                    if nouvel_etat not in nouveaux_etats:
                        nouveaux_etats.add(nouvel_etat)
                        nouveaux_etats_a_traiter.append(nouvel_etat)

        # 🔹 Déterminer les nouveaux états acceptants
        for etat in nouveaux_etats:
            if any(s in self.etats_finaux for s in etat):
                nouveaux_etats_acceptants.add(etat)

        return AutomateDeterministe(nouveaux_etats, nouvelles_transitions, nouvel_etat_initial, nouveaux_etats_acceptants)

    def afficher(self):
        """ Affiche les détails de l'automate """
        print(f"\n🔹 Nombre de symboles : {self.nombre_symboles}")
        print(f"🔹 Nombre d'états : {self.nombre_etats}")
        print(f"🔹 États initiaux : {self.etats_initiaux}")
        print(f"🔹 États finaux : {self.etats_finaux}")
        print(f"🔹 Nombre de transitions : {self.nombre_transitions}")
        print("🔹 Transitions :")
        for (etat, symbole), etats_suivants in self.transitions.items():
            print(f"  {etat} --({symbole})--> {etats_suivants}")

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

class AutomateDeterministe(AutomateFini):
    """ Une version déterminisée de l'automate """
    def __init__(self, etats, transitions, etat_initial, etats_acceptants):
        self.etats = etats
        self.transitions = transitions
        self.etat_initial = etat_initial
        self.etats_acceptants = etats_acceptants
        self.nom_etats = self.renommer_etats()

    def renommer_etats(self):
        """ Génère des noms lisibles pour les états """
        nom_etats = {}
        for i, etat in enumerate(self.etats):
            nom_etats[etat] = f"Q{i}"  # Donne un nom sous forme Q0, Q1, Q2...
        return nom_etats

    def afficher(self):
        """ Affiche les détails de l'automate déterminisé """
        print("\n🔹 Automate Déterminisé :")
        print(f"🔹 Nombre d'états : {len(self.etats)}")
        print(f"🔹 État initial : {self.nom_etats[self.etat_initial]}")
        print(f"🔹 États finaux : {self.etats_acceptants}")
        print("🔹 Transitions :")
        for etat, transitions in self.transitions.items():
            for symbole, destination in transitions.items():
                print(f"  {self.nom_etats[etat]} --({symbole})--> {self.nom_etats[destination]}")


    def acceptedet(self, chaine):

        etats_actuels = {self.etat_initial}  # On commence avec les états initiaux

        for symbole in chaine:
            nouveaux_etats = set()
            for etat in etats_actuels:
                if (etat, symbole) in self.transitions:
                    nouveaux_etats.add(self.transitions[(etat, symbole)])

            if not nouveaux_etats:  # Si aucun nouvel état n'est atteint, la chaîne est rejetée
                return False
            etats_actuels = nouveaux_etats  # Mise à jour des états courants

        # Vérifie si au moins un des états actuels est un état final
        return any(etat in self.etats_acceptants for etat in etats_actuels)

# 🔹 Sélection du fichier
chemin_selectionne = choisir_fichier()
if chemin_selectionne:
     automate = AutomateFini(chemin_selectionne)

automate = AutomateFini(chemin_selectionne)
automate.afficher()

# 🔹 Tester si des chaînes sont acceptées
print("\n🔹 Tests d'acceptation 🔹")
print(f"Chaîne 'a' : {automate.accepte('a')}")
print(f"Chaîne 'bbaaa' : {automate.accepte('bbaaa')}")

#Déterministe, complet ou non
is_deterministe, message = automate.est_deterministe()
print(message)
is_complet,message = automate.is_complet()
print(message)

if is_deterministe == False:
    print("\n🔍 **Suppression des transitions ε et déterminisation**")
    afd = automate.determiniser()
    afd.afficher()

    # 🔹 Tester si des chaînes sont acceptées
    print("\n🔹 Tests d'acceptation 🔹")
    print(f"Chaîne 'a' : {afd.acceptedet('a')}")
    print(f"Chaîne 'bbaaa' : {afd.acceptedet('bbaaa')}")
