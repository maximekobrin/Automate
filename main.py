class AutomateFiniTest:
    def __init__(self):
        # Définir les états, l'état initial et les états finaux
        self.etats = 'q0'
        self.etat_initial = 'q0'
        self.etats_finaux = 'q0'
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q1', 'b': 'q2'},
            'q1': {'a': 'q0', 'b': 'q2'},
            'q2': {'a': 'q1', 'b': 'q0'}
        }
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

class AutomateFini_2:
    def __init__(self):
        # Définir les états, l'état initial et les états finaux
            self.etats = 'q0'
            self.etat_initial = 'q0'
            self.etats_finaux = 'q0'
            # Définir les transitions
            self.transitions = {
                'q0': {'a': 'q0'},
            }

class AutomateFini_3:
    def __init__(self):
        # Définir les états, l'état initial et les états finaux
        self.etats = {'q0'}  # Un seul état
        self.etat_initial = 'q0'
        self.etats_finaux = {'q0'}  # Le même état est aussi final
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q0'},  # L'automate reste dans q0 quand il lit 'a'
        }

class AutomateFini_4:
    def __init__(self):
        # Définir les états, l'état initial et les états finaux
        self.etats = {'q0','q1'}
        self.etat_initial = 'q0'
        self.etats_finaux = set()
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q1'}
        }

class AutomateFini_5:
    def __init__(self):
        self.etats = {'q0','q1','q2','q3','q4'}
        self.etat_initial = {'q0','q3'}
        self.etats_finaux = {'q2','q4'}
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q0', 'b': 'q0'},
            'q1': {'a': 'q2', 'b': 'q0'},
            'q2': {},
            'q3': {'a': 'q0', 'b': 'q4'},
            'q4': {},
        }

class AutomateFini_6:
    def __init__(self):
        self.etats = {'q0','q1','q2','q3'}
        self.etat_initial = {'q1','q3'}
        self.etats_finaux = {'q2','q0'}
        # Définir les transitions
        self.transitions = {
            'q0': {},
            'q1': {'a': 'q2'},
            'q2': {},
            'q3': {'b': 'q0'},
        }

class AutomateFini_7:
    def __init__(self):
        self.etats = {'q0','q1'}
        self.etat_initial = {'q1'}
        self.etats_finaux = {'q0'}
        # Définir les transitions
        self.transitions = {
            'q0': {},
            'q1': {'a': 'q1', 'a' : 'q0'},
        }

class AutomateFini_8:
    def __init__(self):
        self.etats = {'q0','q1'}
        self.etat_initial = {'q1'}
        self.etats_finaux = {'q0'}
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q0'},
            'q1': {'a': 'q0'},
        }

class AutomateFini_19:
    def __init__(self):
        self.etats = {'q0','q1','q2'}
        self.etat_initial = {'q1'}
        self.etats_finaux = {'q0'}
        # Définir les transitions
        self.transitions = {
            'q0': {'a': 'q0'},
            'q1': {'a': 'q2'},
            'q2': {'a': 'q2'},
        }



def accepte(automate, chaine):
    # Vérifier à partir de chaque état initial
    for etat_initial in automate.etat_initial:
        etat_actuel = etat_initial
        for symbole in chaine:
            # Vérifier si l'état actuel a une transition pour le symbole
            if symbole in automate.transitions.get(etat_actuel, {}):
                etat_actuel = automate.transitions[etat_actuel][symbole]
            else:
                break  # Passer à l'état initial suivant
        if etat_actuel in automate.etats_finaux:
            return True
    return False




# Exemple d'utilisation
automate = AutomateFini_8()
print(accepte(automate,"bbaaa")) # True
print(accepte(automate,"a")) # False
