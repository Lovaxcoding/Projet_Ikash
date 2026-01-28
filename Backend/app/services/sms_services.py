from app.utils.sms_parser import parse_mobile_money_sms
from app.models import Transaction
from app.services import transaction_service
from sqlmodel import Session

# Fonction principale pour gérer les SMS entrants
def handle_incoming_sms(sms_text: str):
    # 1. Utilise l'utilitaire de parsing (le moteur Regex)
    parsed_data = parse_mobile_money_sms(sms_text)

    if parsed_data:
        # 2. Ici, on créera plus tard l'objet Transaction pour la DB
        # new_transaction = Transaction(**parsed_data)
        return {"status": "parsed", "data": parsed_data}

    return {"status": "error", "message": "Format inconnu"}

# Service complet pour traiter et enregistrer le SMS
def process_incoming_sms(session: Session, sms_text: str):
    # 1. Analyse du texte via ton moteur Regex (Contrôleur métier)
    parsed_data = parse_mobile_money_sms(sms_text)

    if not parsed_data:
        return {"status": "error", "message": "Format SMS inconnu"}

    # 2. Conversion des données parsées en Modèle Transaction
    # On déballe le dictionnaire parsed_data directement dans le modèle
    try:
        new_transaction = Transaction(**parsed_data)

        # 3. Appel du service de transaction pour la sauvegarde (Le "M" de MVC)
        db_transaction = transaction_service.create_transaction(
            session, new_transaction
        )

        return {
            "status": "success",
            "message": "Transaction enregistrée",
            "data": db_transaction,
        }
    except Exception as e:
        return {"status": "error", "message": f"Échec de création : {str(e)}"}
