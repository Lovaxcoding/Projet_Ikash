import re
from typing import Optional, Dict


def parse_mobile_money_sms(sms_text: str) -> Optional[Dict]:
    # Exemple pour un SMS type : "Transfert reçu de 0340000000. Montant: 50000Ar. Ref: 12345678"

    # On cherche le montant (chiffres suivis de Ar ou MGA)
    montant_match = re.search(r"Montant[:\s]+(\d+[\d\s]*)", sms_text)
    # On cherche la référence
    ref_match = re.search(r"Ref[:\s]+(\w+)", sms_text)
    # On cherche l'expéditeur (numéro de téléphone)
    sender_match = re.search(r"de\s+(\d{10})", sms_text)

    if montant_match and ref_match:
        # On nettoie le montant (enlever les espaces si "50 000")
        montant = float(montant_match.group(1).replace(" ", ""))

        return {
            "montant": montant,
            "reference_sms": ref_match.group(1),
            "type_op": "RECEPTION",
            "agent_id": sender_match.group(1) if sender_match else "UNKNOWN",
        }

    return None
