from app.services.parser import parser_iptables_save
from app.services.generateur import generer_iptables_restore

texte_original = """*filter
:INPUT DROP [0:0]
-A INPUT -p icmp --icmp-type echo-request -j DROP
COMMIT"""

tables = parser_iptables_save(texte_original)
texte_regenere = generer_iptables_restore(tables)

print(texte_regenere)