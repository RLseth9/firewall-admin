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
    regle_existe_deja_systeme,
)
from app.services.parser import parser_iptables_save, obtenir_resume_chaines,regle_existe_deja
from app.services.generateur import generer_iptables_restore, generer_commande_regle_unique
from app.models.iptables import Table, Regle

router = APIRouter()


@router.get("/local/regles")
def obtenir_regles_locales():
    """Lit et retourne TOUTES les regles actuelles de la machine locale."""
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)
    return tables


@router.post("/local/regles")
def modifier_regles_locales(tables: List[Table]):
    """REMPLACEMENT COMPLET : ecrase toute la configuration actuelle."""
    texte_genere = generer_iptables_restore(tables)
    appliquer_regles_locales(texte_genere)
    return {"message": "Regles appliquees avec succes"}


@router.post("/local/regles/une")
def ajouter_une_regle(regle: Regle):
    """
    AJOUT CIBLE : ajoute une seule regle, sans toucher au reste
    de la configuration actuelle. Usage quotidien.
    """
    if regle_existe_deja_systeme(regle):
        return {"message": "Cette regle existe deja, aucune action effectuee"}

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


@router.get("/local/chaines")
def obtenir_liste_chaines():
    """Retourne un resume leger de toutes les chaines disponibles (sans le detail des regles)."""
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)
    return obtenir_resume_chaines(tables)


@router.get("/local/tout")
def obtenir_regles_et_resume():
    """Retourne a la fois le detail complet ET le resume, en une seule lecture systeme."""
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)

    return {
        "detail": tables,
        "resume": obtenir_resume_chaines(tables)
    }

@router.post("/local/regles/une/apercu")
def apercu_commande_regle(regle: Regle, mode: str):
    """
    Genere et retourne la commande iptables SANS l'executer.
    verification de la commande avec l'execution 
    """
    commande = generer_commande_regle_unique(regle, mode=mode)
    return {"commande": " ".join(commande)}
@router.post("/local/regles/une")
def ajouter_une_regle(regle: Regle):
    """
    AJOUT CIBLE : ajoute une seule regle, sans toucher au reste
    de la configuration actuelle. Refuse si une regle identique existe deja.
    """
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)

    if regle_existe_deja(regle, tables):
        return {"message": "Cette regle existe deja, aucune action effectuee"}

    ajouter_regle_locale(regle)
    return {"message": "Regle ajoutee avec succes"}