from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.models import Transaction
from app.services import transaction_service
import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# On définit où on attend la clé (ici dans un header nommé 'X-API-KEY')
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("API_SECRET_KEY"):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé : Clé API invalide"
    )


router = APIRouter(prefix="/transactions", tags=["Transactions"])


# Dépendance pour obtenir la session de la DB
def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=Transaction)
def add_transaction(transaction: Transaction, session: Session = Depends(get_session), api_key: str = Depends(get_api_key)):
    try:
        return transaction_service.create_transaction(session, transaction)
    except Exception as e:
        # On utilise f"" pour injecter la variable str(e)
        raise HTTPException(
            status_code=400, detail=f"Erreur lors de l'ajout : {str(e)}"
        )


@router.get("/")
def list_transactions(session: Session = Depends(get_session)):
    return transaction_service.get_all_transactions(session)
