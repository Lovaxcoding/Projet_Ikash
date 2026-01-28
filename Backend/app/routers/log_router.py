from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from app.models.log import LogActivite
from app.security.get_api_key import get_api_key
from app.database import engine
from typing import List, Optional
from uuid import UUID

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/", response_model=List[LogActivite])
def get_logs(
    admin_id: Optional[UUID] = None,  # Optionnel : filtrer pour un admin précis
    limit: int = Query(default=100, le=500),  # Sécurité pour ne pas faire ramer la DB
    api_key: str = Depends(get_api_key),
):
    with Session(engine) as session:
        # On prépare la requête
        statement = (
            select(LogActivite).order_by(LogActivite.horodatage.desc()).limit(limit)
        )

        # Si on passe un admin_id, on filtre les résultats
        if admin_id:
            statement = statement.where(LogActivite.admin_id == admin_id)

        results = session.exec(statement).all()
        return results
