from sqlmodel import Session, select
from app.models import Profile
from app.models.enums import RoleType
from uuid import UUID
from typing import List, Optional


def create_new_profile(session: Session, profile_data: Profile) -> Profile:
    """
    Crée un profil (Admin ou Agent).
    Si c'est un agent, il doit idéalement avoir un admin_id.
    """
    session.add(profile_data)
    session.commit()
    session.refresh(profile_data)
    return profile_data


def get_agents_by_admin(session: Session, admin_id: UUID) -> List[Profile]:
    """
    Récupère tous les agents liés à un administrateur spécifique.
    C'est le cœur du Multi-Tenancy pour le tableau de bord du Boss.
    """
    statement = select(Profile).where(
        Profile.admin_id == admin_id, Profile.role == RoleType.AGENT
    )
    return session.exec(statement).all()


def update_agent_balance(session: Session, agent_id: UUID, amount: float):
    """
    Utile plus tard pour mettre à jour le solde après une transaction.
    """
    agent = session.get(Profile, agent_id)
    if agent:
        agent.solde_courant += amount
        session.add(agent)
        session.commit()
        session.refresh(agent)
    return agent
