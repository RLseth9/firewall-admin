"""
    transformation de sortie de iptable-save en objet python 
"""

from app.models.iptables import ResumeChaine,Condition, Regle, Chaine, Table
from typing import List
import   shlex


def parser_iptables_save(texte: str) -> List[Table]:
    tables = []
    table_courante = None
    compteur_regle_id = 1

    lignes = texte.strip().split("\n")

    for ligne in lignes:
        ligne = ligne.strip()

        if not ligne or ligne.startswith("#"):
            continue

        if ligne.startswith("*"):
            nom_table = ligne[1:]
            table_courante = Table(nom=nom_table, chaines=[])
            tables.append(table_courante)

        elif ligne.startswith(":"):
            sans_deux_points = ligne[1:]
            morceaux = sans_deux_points.split()
            nom_chaine = morceaux[0]
            policy = morceaux[1]
            nouvelle_chaine = Chaine(nom=nom_chaine, policy_defaut=policy, regles=[])
            table_courante.chaines.append(nouvelle_chaine)

        elif ligne.startswith("-A"):
          #  morceaux = ligne.split()
            morceaux = shlex.split(ligne) 

            nom_chaine_cible = morceaux[1]

            conditions = []
            action = None
            negation_en_attente = False

            i = 2
            while i < len(morceaux):
                token = morceaux[i]

                if token == "!":
                    negation_en_attente = True
                    i += 1
                    continue

                if token == "-j":
                    action = morceaux[i + 1]
                    i += 2
                    continue

                type_condition = token.lstrip("-")
                valeur_existe = (i +1 < len(morceaux)) and (not morceaux[i + 1].startswith("-"))
                
                if valeur_existe:
                    valeur = morceaux[i + 1]
                    if negation_en_attente:
                        valeur = "! " + valeur
                        negation_en_attente = False
                    conditions.append(Condition(type=type_condition, valeur=valeur))
                    i += 2
                else:
                    # Option "drapeau" sans valeur (ex: --random-fully, --physdev-is-bridged)
                    conditions.append(Condition(type=type_condition, valeur=""))
                    negation_en_attente = False
                    i += 1
                 


            chaine_cible = None
            for c in table_courante.chaines:
                if c.nom == nom_chaine_cible:
                    chaine_cible = c
                    break

            position = len(chaine_cible.regles) + 1

            nouvelle_regle = Regle(
                id=compteur_regle_id,
                chaine=nom_chaine_cible,
                action=action,
                position=position,
                conditions=conditions
            )

            chaine_cible.regles.append(nouvelle_regle)
            compteur_regle_id += 1

        elif ligne == "COMMIT":
            table_courante = None

    return tables

def obtenir_resume_chaines(tables: list) -> list:
    """
    Construit un resume leger (table, chaine, policy, nombre de regles)
    a partir de la liste complete des objets Table.
    Utile pour peupler une interface sans transferer tout le detail.
    """
    resumes = []

    for table in tables:
        for chaine in table.chaines:
            resume = ResumeChaine(
                table=table.nom,
                nom_chaine=chaine.nom,
                policy_defaut=chaine.policy_defaut,
                nombre_regles=len(chaine.regles)
            )
            resumes.append(resume)

    return resumes