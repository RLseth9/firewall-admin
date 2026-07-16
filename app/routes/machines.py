"""
Routes API pour la gestion des regles iptables de la machine locale.
"""

from typing import List
from fastapi import APIRouter
from app.services.executeur import (
    lire_regles_locales,
    appliquer_regles_locales,
    ajouter_regle_locale,
    supprimer_regle_locale,
)
from app.services.parser import parser_iptables_save
from app.services.generateur import generer_iptables_restore
from app.models.iptables import Table, Regle

router = APIRouter()

#get :pour affichage 
@router.get("/local/regles")
def obtenir_regles_locales():
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)
    return tables

#post : MAJ
@router.post("/local/regles")
def modifier_regles_locales(tables: List[Table]):
    texte_genere = generer_iptables_restore(tables)
    appliquer_regles_locales(texte_genere)
    return {"message": "Regles appliquees avec succes"}


@router.post("/local/regles/une")
def ajouter_une_regle(regle: Regle):
    """
    AJOUT CIBLE : ajoute une seule regle, sans toucher au reste
    de la configuration actuelle. Usage quotidien.
    """
    ajouter_regle_locale(regle)
    return {"message": "Regle ajoutee avec succes"}


@router.delete("/local/regles/une")
def supprimer_une_regle(regle: Regle):
    """
    SUPPRESSION CIBLEE : supprime une seule regle precise,
    sans toucher au reste de la configuration actuelle. Usage quotidien.
    """
    supprimer_regle_locale(regle)
    return {"message": "Regle supprimee avec succes"}