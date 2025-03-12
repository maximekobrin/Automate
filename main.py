class AutomateFini_1:
    def __init__(self):
        # Définir les états, l'état initial et les états finaux
        self.etats = 'q0'
        self.etat_initial = 'q0'
        self.etats_finaux = 'q0'
        # Définir les transitions
        self.transitions = {}

    def accepte(self, chaine):
        etat_actuel = self.etat_initial
        for symbole in chaine:
            if symbole in self.transitions[etat_actuel]:
                etat_actuel = self.transitions[etat_actuel][symbole]
            else:
                return False
        return etat_actuel in self.etats_finaux


