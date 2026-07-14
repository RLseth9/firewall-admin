"""
Module de generation de texte iptables-restore a partir des objets Python.
Fait l'operation inverse du parser.
"""

from app.models.iptables import Table


def _prefixe_option(type_condition: str) -> str:
    """
    Ajoute le bon nombre de tirets devant une option,
    selon la convention iptables (1 lettre = un tiret, sinon deux).
    """
    if len(type_condition) == 1:
        return "-" + type_condition
    return "--" + type_condition


def _generer_ligne_regle(regle) -> str:
    """Reconstruit une seule ligne '-A ...' a partir d'un objet Regle."""

    morceaux = ["-A", regle.chaine]

    for condition in regle.conditions:
        option = _prefixe_option(condition.type)

        # Gestion de la negation stockee avec "! " au debut de la valeur
        if condition.valeur.startswith("! "):
            morceaux.append("!")
            valeur_reelle = condition.valeur[2:]  # on enleve "! "
        else:
            valeur_reelle = condition.valeur

        morceaux.append(option)

        # Si la valeur n'est pas vide, on l'ajoute (sinon c'etait un drapeau seul)
        if valeur_reelle != "":
            morceaux.append(valeur_reelle)

    morceaux.append("-j")
    morceaux.append(regle.action)

    return " ".join(morceaux)


def generer_iptables_restore(tables: list[Table]) -> str:
    """
    Reconstruit le texte complet iptables-restore
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