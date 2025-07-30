import os
import json
from dateutil.parser import parse

# Obtenir le répertoire actuel du script
current_directory = os.path.dirname(os.path.abspath(__file__))
coefficients_file_path = os.path.join(current_directory, 'coefficients.json')

def get_TURPE_coef(date, version_utilisation, domaine_tension):
        date = parse(date).date()  # Convertit la chaîne de caractères en objet datetime.date
        with open(coefficients_file_path, 'r') as fichier:
            donnees = json.load(fichier)

        for coefficient in donnees["coefficients"]:
            start_date = parse(coefficient["start_date"]).date()
            expiration_date = parse(coefficient["expiration_date"]).date()
            if (start_date <= date <= expiration_date and
                coefficient["version_utilisation"] == version_utilisation and
                coefficient["domaine_tension"] == domaine_tension):
                return coefficient

        return None

# Utilisation de la fonction pour trouver l'instance
date_recherchee = "2023-01-01"
version_recherchee = "LU_pf"
domaine_recherche = "HTA"

coefficient_trouve = get_TURPE_coef(date_recherchee, version_recherchee, domaine_recherche)

if coefficient_trouve:
    print("Coefficient trouvé:")
    print(coefficient_trouve)
else:
    print("Aucun coefficient trouvé pour les conditions spécifiées.")
