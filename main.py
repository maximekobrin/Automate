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
        """ Calcule la fermeture ε d'un état """
        fermeture = {etat}  # L'état fait partie de sa propre fermeture ε
        pile = [etat]  # Pile pour explorer les transitions ε

        while pile:
            etat_courant = pile.pop()
            if (etat_courant, "ε") in self.transitions:  # Vérifie si ε-transition existe
                for voisin in self.transitions[(etat_courant, "ε")]:
                    if voisin not in fermeture:
                        fermeture.add(voisin)
                        pile.append(voisin)  # Ajoute le voisin pour continuer l'exploration

        return fermeture  # Retourne l'ensemble des états accessibles par ε

    #elimination des ε-transition
    def eliminer_transitions_epsilon(self):
        nouvelles_transitions = defaultdict(set)
        fermeture_epsilon = {etat: self.fermeture_epsilon(etat) for etat in self.etats}

        # Reconstruction des transitions sans ε
        for (etat, symbole), destinations in self.transitions.items():
            if symbole != "ε":
                for destination in destinations:
                    for etat_f in fermeture_epsilon[etat]:
                        nouvelles_transitions[(etat_f, symbole)].update(fermeture_epsilon[destination])

        # Conserver toutes les transitions normales
        for (etat, symbole), destinations in self.transitions.items():
            if symbole != "ε":
                nouvelles_transitions[(etat, symbole)].update(destinations)

        # Mise à jour des états finaux
        nouveaux_etats_finaux = set()
        for etat in self.etats:
            if any(f in self.etats_finaux for f in fermeture_epsilon[etat]):
                nouveaux_etats_finaux.add(etat)

        # Mise à jour de l'automate
        self.transitions = nouvelles_transitions
        self.etats_finaux = nouveaux_etats_finaux
        print("\nLes transitions ε ont été éliminées et l'automate est mis à jour.")

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
        return any(symbole == "ε" for _, symbole in self.transitions.keys())


    def is_standard(self):
        if len(self.etats_initiaux) != 1:
            return False

        etat_initial = next(iter(self.etats_initiaux))

        for (etat_depart,symbole), etats_arrivee in self.transitions.items():
            if etat_initial in etats_arrivee or etat_depart != etat_initial:
                return False

        return True

    def standardiser(self):

        if self.is_standard():
            print("L'automate est déjà standard.")
            return self

        nouvel_etat_initial = "état_i"


        self.etats.add(nouvel_etat_initial)


        for etat_initial in self.etats_initiaux:
            self.transitions.setdefault((nouvel_etat_initial, ""), set()).add(etat_initial)


            for (etat_depart, symbole), etats_arrivee in list(self.transitions.items()):
                if etat_depart == etat_initial:
                    self.transitions.setdefault((nouvel_etat_initial, symbole), set()).update(etats_arrivee)

        # Mettre à jour l'état initial
        self.etats_initiaux = {nouvel_etat_initial}

        print("Standardisation terminée.")

    def minimiser(self):
        def refine_partitions(partitions):
            nouvelle_partition = []
            for partition in partitions:
                # Dictionnaire pour regrouper les états par leurs transitions
                transition_dict = defaultdict(set)
                for etat in partition:
                    # Obtenir les transitions pour chaque symbole
                    for symbole in {s for (e, s) in self.transitions.keys() if e == etat}:
                        destination = self.transitions.get((etat, symbole), set())
                        transition_dict[frozenset(destination)].add(etat)
                nouvelle_partition.extend(transition_dict.values())
            return nouvelle_partition
        # 1. Identifier les états acceptants et non acceptants
        etats_acceptants = self.etats_finaux
        etats_non_acceptants = self.etats - etats_acceptants
        # 2. Créer des partitions initiales
        partitions = [etats_acceptants, etats_non_acceptants]
        partitions = [set(partition) for partition in partitions if partition]  # Supprimer les partitions vides
        # Affiner jusqu'à ce qu'il n'y ait plus de changements
        while True:
            nouvelles_partitions = refine_partitions(partitions)
            if len(nouvelles_partitions) == len(partitions):
                break
            partitions = nouvelles_partitions
        def refine_partitions(partitions):
            nouvelle_partition = []
            for partition in partitions:
                # Dictionnaire pour regrouper les états par leurs transitions
                transition_dict = defaultdict(set)
                for etat in partition:
                    # Obtenir les transitions pour chaque symbole
                    for symbole in {s for (e, s) in self.transitions.keys() if e == etat}:
                        destination = self.transitions.get((etat, symbole), set())
                        transition_dict[frozenset(destination)].add(etat)
                nouvelle_partition.extend(transition_dict.values())
            return nouvelle_partition
        # 4. Créer l'automate minimisé
        nouveaux_etats = {frozenset(partition) for partition in partitions}
        nouvel_etat_initial = frozenset(self.etats_initiaux)
        nouvelles_transitions = {}
        # Créer les nouvelles transitions
        for partition in partitions:
            for etat in partition:
                for symbole in {s for (e, s) in self.transitions.keys() if e == etat}:
                    destination = self.transitions.get((etat, symbole), set())
                    destination_partition = frozenset(next(p for p in partitions if etat in p))
                    nouvelles_transitions.setdefault((frozenset(partition), symbole), set()).add(destination_partition)
        # Créer et retourner un nouvel automate déterministe
        return AutomateDeterministe(nouveaux_etats, nouvelles_transitions, nouvel_etat_initial,
                                    {frozenset(part) for part in partitions if part & etats_acceptants})

    def complémentaire(self):
        nouveaux_etats_finaux = self.etats - self.etats_finaux
        self.etats_finaux = nouveaux_etats_finaux

        print("Transformation en langage complémentaire terminée.")

    def determiniser(self):
        def format_etat(etat):
            return "{" + ", ".join(sorted(etat)) + "}" if etat else "∅"

        if self.contient_transition_epsilon():
            self.eliminer_transitions_epsilon()
        else:
            print("Pas de relation ε, donc déterminisation directe.")

        nouvel_etat_initial = frozenset(self.etats_initiaux)
        print(f"Nouvel état initial : {format_etat(nouvel_etat_initial)}")

        nouveaux_etats = {nouvel_etat_initial}
        nouveaux_etats_a_traiter = [nouvel_etat_initial]
        nouvelles_transitions = {}
        nouveaux_etats_acceptants = set()

        alphabet = {s for _, s in self.transitions.keys() if s != "ε"}
        print(f"Alphabet : {alphabet}")
        print("Transition :  \n")

        while nouveaux_etats_a_traiter:
            etat_courant = nouveaux_etats_a_traiter.pop()

            nouvelles_transitions[etat_courant] = {}


            # Parcours de l'alphabet
            for symbole in alphabet:
                nouvel_etat = set()
                # Recherche des états de transition pour chaque état dans etat_courant
                for etat in etat_courant:
                    if (etat, symbole) in self.transitions:
                        nouvel_etat.update(self.transitions[(etat, symbole)])

                # Convertir nouvel_etat en frozenset (ensemble immuable)
                nouvel_etat = frozenset(nouvel_etat)
                if nouvel_etat:
                    nouvelles_transitions[etat_courant][symbole] = nouvel_etat

                    if nouvel_etat not in nouveaux_etats:
                        nouveaux_etats.add(nouvel_etat)
                        nouveaux_etats_a_traiter.append(nouvel_etat)

        # Déterminer les nouveaux états acceptants
        for etat in nouveaux_etats:
            if any(s in self.etats_finaux for s in etat):
                nouveaux_etats_acceptants.add(etat)



        for etat, transitions in nouvelles_transitions.items():
            etat_formatte = format_etat(etat)
            for symbole, destination in transitions.items():
                print(f"{etat_formatte} -- {symbole} --> {format_etat(destination)}")

        print(" ")
        # Retourner un nouvel automate déterministe
        return AutomateDeterministe(
            {format_etat(etat) for etat in nouveaux_etats},
            {format_etat(e): {symb: format_etat(dest) for symb, dest in trans.items()} for e, trans in
             nouvelles_transitions.items()},
            format_etat(nouvel_etat_initial),
            {format_etat(e) for e in nouveaux_etats_acceptants}
        )

    def afficher(self):
        """ Affiche les détails de l'automate """
        print(f"\nNombre de symboles : {self.nombre_symboles}")
        print(f"Nombre d'états : {self.nombre_etats}")
        print(f"États initiaux : {self.etats_initiaux}")
        print(f"États finaux : {self.etats_finaux}")
        print(f"Nombre de transitions : {self.nombre_transitions}\n")

    def afficher_table_transitions(self):
        if not self.transitions:
            print("\nAucune table de transition définie.")
            return

        # Récupérer l'alphabet sans ε
        alphabet = sorted(
            {s for key in self.transitions.keys() if isinstance(key, tuple) and len(key) == 2 for _, s in [key] if
             s != "ε"})

        largeur_etat = max(len(str(etat)) for etat in self.etats) + 6  # Espacement pour (I) ou (F)
        largeur_symbole = (max((len(symbole) for symbole in alphabet), default=1)) + 7
        largeur_colonne = max(largeur_etat, largeur_symbole)

        # Affichage de l'en-tête
        print("\nTable de transition :")
        en_tete = "État".ljust(largeur_colonne) + "".join(symbole.ljust(largeur_colonne) for symbole in alphabet)
        print("-" * len(en_tete))
        print(en_tete)
        print("-" * len(en_tete))

        # Affichage des transitions
        for etat in sorted(self.etats, key=str):

            type_etat = ""
            if etat in self.etats_initiaux and etat in self.etats_finaux:
                type_etat = "(I,F)"
            elif etat in self.etats_initiaux:
                type_etat = "(I)"
            elif etat in self.etats_finaux:
                type_etat = "(F)"

            ligne = f"{type_etat}{etat}".ljust(largeur_colonne)

            for symbole in alphabet:
                destination = self.transitions.get((etat, symbole), "∅")  # "∅" si aucune transition
                destination_str = ",     ".join(destination) if isinstance(destination, set) else destination
                ligne += destination_str.ljust(largeur_colonne)  # Aligner les colonnes

            print(ligne)

        print("-" * len(en_tete))

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
    def __init__(self, etats, transitions, etat_initial, etats_acceptants):
        self.etats = etats
        self.transitions = transitions
        self.etat_initial = etat_initial
        self.etats_acceptants = etats_acceptants
        self.nom_etats = self.renommer_etats()

    def complémentaire(self):
        nouveaux_etats_finaux = self.etats - self.etats_acceptants
        self.etats_acceptants = nouveaux_etats_finaux

        print("Transformation en langage complémentaire terminée.")

    def renommer_etats(self):
        nom_etats = {}
        for i, etat in enumerate(self.etats):
            nom_etats[etat] = f"Q{i}"  # Donne un nom sous forme Q0, Q1, Q2...
        return nom_etats

    def afficher(self):

        print(f"Nombre d'états : {len(self.etats)}")
        print(f"État initial : {self.etat_initial}")
        print(f"États finaux : {self.etats_acceptants}")



    def minimiser(self):
        def refine_partitions(partitions):
            nouvelle_partition = []
            for partition in partitions:
                # Dictionnaire pour regrouper les états par leurs transitions
                transition_dict = defaultdict(set)
                for etat in partition:
                    # Obtenir les transitions pour chaque symbole
                    for symbole in {s for (e, s) in self.transitions.keys() if e == etat}:
                        destination = self.transitions.get((etat, symbole), set())
                        transition_dict[frozenset(destination)].add(etat)
                nouvelle_partition.extend(transition_dict.values())
            return nouvelle_partition
        # 1. Identifier les états acceptants et non acceptants
        etats_acceptants = self.etats_finaux
        etats_non_acceptants = self.etats - etats_acceptants
        # 2. Créer des partitions initiales
        partitions = [etats_acceptants, etats_non_acceptants]
        partitions = [set(partition) for partition in partitions if partition]  # Supprimer les partitions vides
         # Affiner jusqu'à ce qu'il n'y ait plus de changements
        while True:
            nouvelles_partitions = refine_partitions(partitions)
            if len(nouvelles_partitions) == len(partitions):
                break
            partitions = nouvelles_partitions
        # 4. Créer l'automate minimisé
        nouveaux_etats = {frozenset(partition) for partition in partitions}
        nouvel_etat_initial = frozenset(self.etats_initiaux)
        nouvelles_transitions = {}
        # Créer les nouvelles transitions
        for partition in partitions:
            for etat in partition:
                for symbole in {s for (e, s) in self.transitions.keys() if e == etat}:
                    destination = self.transitions.get((etat, symbole), set())
                    destination_partition = frozenset(next(p for p in partitions if etat in p))
                    nouvelles_transitions.setdefault((frozenset(partition), symbole), set()).add(destination_partition)
        # Créer et retourner un nouvel automate déterministe
        return AutomateDeterministe(nouveaux_etats, nouvelles_transitions, nouvel_etat_initial,
                                    {frozenset(part) for part in partitions if part & etats_acceptants})



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


# 🔹 Menu interactif
print("\nBienvenue dans le menu des automates !")

while True:
    chemin_selectionne = choisir_fichier()
    if not chemin_selectionne:
        print("Aucun fichier sélectionné. Arrêt du programme.")
        break

    # Charger et afficher l'automate
    automate = AutomateFini(chemin_selectionne)
    automate.afficher()
    automate.afficher_table_transitions()

    while True:
        print("\n🔹 Que voulez-vous faire ?")
        print("1️⃣ Standardiser l'automate")
        print("2️⃣ Déterminiser l'automate")
        print("3️⃣ Complémenter l'automate")
        print("4️⃣ Minimiser l'automate")
        print("5️⃣ Changer d'automate")
        print("6 Tester un mot")
        print("7 Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            is_standard = automate.is_standard()
            standard = automate.standardiser()
            automate.afficher()
            automate.afficher_table_transitions()

        elif choix == "2":
            is_deterministe, message = automate.est_deterministe()
            print(message)
            if not is_deterministe:
                automate = automate.determiniser()
                automate.afficher()


        elif choix == "3":
            automate.complémentaire()
            automate.afficher()

        elif choix == "4":
            mini = automate.minimiser()
            automate.afficher()


        elif choix == "5":
            break  # Permet de relancer la sélection d'un automate

        elif choix == "6":
            print("Test de mot")
            mot = input("Quels mots souhaitez-vous essayer : ")
            print(f"Chaîne '{mot}' : {automate.accepte(mot)}")


        elif choix == "7":
            print("✅ Programme terminé.")
            exit()

        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")