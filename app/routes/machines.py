from fastapi import APIRouter
from app.services.executeur import lire_regles_locales
from app.services.parser import parser_iptables_save

router = APIRouter()


@router.get("/local/regles")
def obtenir_regles_locales():
    texte_brut = lire_regles_locales()
    tables = parser_iptables_save(texte_brut)
    return tables