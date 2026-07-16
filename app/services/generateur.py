"""
iptable-save en iptable-restore :  objets python en texte 
"""

from app.models.iptables import Table
from app.models.iptables import Regle


def _prefixe_option(type_condition: str) -> str:
    """
    fonction qui ajoute les tirets sur les options: un carctère = 1 tiret , +1 caratère = 2 tirets
    """
    if len(type_condition) == 1:
        return "-" + type_condition
    return "--" + type_condition
def _generer_morceaux_conditions(regle: Regle) -> list[str]:
    """
    Construit la liste des morceaux (options + valeurs) pour les conditions
    d'une regle. Reutilise pour -A (ajout) et -D (suppression), qui partagent
    exactement la meme logique de conditions.
    """
    morceaux = []

    for condition in regle.conditions:
        option = _prefixe_option(condition.type)

        if condition.valeur.startswith("! "):
            morceaux.append("!")
            valeur_reelle = condition.valeur[2:]
        else:
            valeur_reelle = condition.valeur

        morceaux.append(option)

        if valeur_reelle != "":
            morceaux.append(valeur_reelle)

    return morceaux


def _generer_ligne_regle(regle) -> str:
    """Reconstruition d'une  ligne '-A ...' a partir d'un objet Regle."""
    """Reconstruit une seule ligne '-A ...' a partir d'un objet Regle."""
    morceaux = ["-A", regle.chaine]
    morceaux += _generer_morceaux_conditions(regle)
    morceaux.append("-j")
    morceaux.append(regle.action)
    return " ".join(morceaux)

   

    return " ".join(morceaux)


def generer_iptables_restore(tables: list[Table]) -> str:
    """
    Reconstruition du texte complet iptables-restore
    a partir de la liste d'objets Table.
    """
    lignes = []

    for table in tables:
        lignes.append(f"*{table.nom}")

        for chaine in table.chaines:
            lignes.append(f":{chaine.nom} {chaine.policy_defaut} [0:0]")

        for chaine in table.chaines:
            for regle in chaine.regles:
                lignes.append(_generer_ligne_regle(regle))

        lignes.append("COMMIT")

    return "\n".join(lignes) + "\n"
def generer_commande_regle_unique(regle: Regle, mode: str) -> list[str]:
    """
    Genere une commande iptables complete (sous forme de LISTE d'arguments,
    pas une chaine de texte) pour ajouter ou supprimer UNE SEULE regle.

    mode doit valoir "ajouter" ou "supprimer".
    Retourne une liste utilisable directement par subprocess.run(),
    ex: ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-j", "ACCEPT"]
    """
    if mode == "ajouter":
        drapeau_action = "-A"
    elif mode == "supprimer":
        drapeau_action = "-D"
    else:
        raise ValueError(f"mode invalide: {mode} (attendu: 'ajouter' ou 'supprimer')")

    commande = ["iptables", drapeau_action, regle.chaine]
    commande += _generer_morceaux_conditions(regle)
    commande.append("-j")
    commande.append(regle.action)

    return commande