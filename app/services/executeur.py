"""
CODE pour communication direct avec le système
"""

import subprocess
from app.models.iptables import Regle
from app.services.generateur import generer_commande_regle_unique



class IptablesError(Exception):
    """Exception levée quand une commande iptables échoue."""


def lire_regles_locales() -> str:
    """
    Execution 'iptables-save' sur la machine locale et retourne
    le texte brut produit, tel quel.
    """
    try:
        resultat = subprocess.run(
            ["iptables-save"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as erreur:
        raise IptablesError(f"Erreur iptables-save: {erreur.stderr}") from erreur

    return resultat.stdout
def appliquer_regles_locales(texte_iptables_restore: str) -> None:
    """
    Applique un texte au format iptables-restore sur la machine locale.
    Remplace INTEGRALEMENT la configuration iptables actuelle du machine 
    """
    try:
        subprocess.run(
            ["iptables-restore"],
            input=texte_iptables_restore,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as erreur:
        raise IptablesError(f"Erreur iptables-restore: {erreur.stderr}") from erreur
    

def ajouter_regle_locale(regle: Regle) -> None:
    """
    Ajoute UNE regle precise a la configuration actuelle,
    sans toucher aux autres regles deja en place.
    """
    commande = generer_commande_regle_unique(regle, mode="ajouter")

    try:
        subprocess.run(
            commande,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as erreur:
        raise IptablesError(f"Erreur lors de l'ajout de la regle: {erreur.stderr}") from erreur


def supprimer_regle_locale(regle: Regle) -> None:
    """
    Supprime UNE regle precise de la configuration actuelle,
    sans toucher aux autres regles deja en place.
    """
    commande = generer_commande_regle_unique(regle, mode="supprimer")

    try:
        subprocess.run(
            commande,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as erreur:
        raise IptablesError(f"Erreur lors de la suppression de la regle: {erreur.stderr}") from erreur