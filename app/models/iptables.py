"""
Modele de donnees representant la structure iptables :
Table -> Chaine -> Regle -> Condition, plus un resume leger.
"""

from typing import List
from pydantic import BaseModel


class Condition(BaseModel):
    """Une condition unique appliquee a une regle (ex: protocole, port)."""
    type: str
    valeur: str


class Regle(BaseModel):
    """Une regle iptables complete, avec sa liste de conditions."""
    id: int
    chaine: str
    action: str
    position: int
    conditions: List[Condition]


class Chaine(BaseModel):
    """Une chaine iptables (INPUT, OUTPUT, FORWARD...) et ses regles."""
    nom: str
    policy_defaut: str
    regles: List[Regle] = []


class Table(BaseModel):
    """Une table iptables (filter, nat, mangle...) et ses chaines."""
    nom: str
    chaines: List[Chaine] = []


class ResumeChaine(BaseModel):
    """Vue allegee d'une chaine, sans le detail des regles."""
    table: str
    nom_chaine: str
    policy_defaut: str
    nombre_regles: int