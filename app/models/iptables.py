from pydantic import BaseModel
from typing import List


class Condition(BaseModel):
    type: str
    valeur: str


class Regle(BaseModel):
    id: int
    chaine: str
    action: str
    position: int
    conditions: List[Condition]


class Chaine(BaseModel):
    nom: str
    policy_defaut: str
    regles: List[Regle] = []


class Table(BaseModel):
    nom: str
    chaines: List[Chaine] = []