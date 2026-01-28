from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import engine
from app.models import Profile
from typing import List
from app.services import profile_service
from app.security.get_api_key import get_api_key

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Dépendance pour obtenir la session de la DB
@router.get("/", response_model=List[Profile])
def get_profiles():
    with Session(engine) as session:
        # Pour l'instant on renvoie tout pour tester
        return session.query(Profile).all()


# Route pour créer un nouveau profil
@router.post("/")
def create_profile(profile: Profile, api_key: str = Depends(get_api_key)):
    with Session(engine) as session:
        return profile_service.create_new_profile(session, profile)
