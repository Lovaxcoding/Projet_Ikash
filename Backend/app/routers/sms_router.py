from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlmodel import Session
from app.database import engine
from app.services import sms_services
from app.security.get_api_key import get_api_key
import os

router = APIRouter(prefix="/sms", tags=["SMS Receiver"])


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/receive")
async def receive_and_parse_sms(
    payload: dict,
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key),
):
    try:
        # On extrait le texte du JSON reçu (ex: {"text": "Transfert reçu..."})
        sms_text = payload.get("text")
        if not sms_text:
            raise HTTPException(status_code=400, detail="Contenu SMS manquant")

        # On délègue tout le travail au service
        return sms_services.process_incoming_sms(session, sms_text)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erreur lors du traitement SMS : {str(e)}"
        )
