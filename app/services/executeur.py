"""
Module d'exécution des commandes iptables sur la machine locale.

Ce service est responsable de communiquer directement avec le système
d'exploitation pour lire ou modifier la configuration iptables active.
"""

import subprocess


class IptablesError(Exception):
    """Exception levée quand une commande iptables échoue."""


def lire_regles_locales() -> str:
    """
    Execute 'iptables-save' sur la machine locale et retourne
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