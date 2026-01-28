from sqlmodel import Session, select
from app.models import Profile
from app.models.enums import RoleType
from uuid import UUID
from typing import List, Optional
from app.models.log import LogActivite

# Service pour gérer les profils (Admins et Agents)
def update_agent_balance_with_log(session: Session, admin_id: UUID, agent_id: UUID, amount: float):
    agent = session.get(Profile, agent_id)
    if not agent:
        return None

    ancien = agent.solde_courant
    agent.solde_courant += amount
    nouveau = agent.solde_courant

    # On crée le log
    log = LogActivite(
        admin_id=admin_id,
        agent_id=agent_id,
        action="MODIFICATION_SOLDE",
        ancien_solde=ancien,
        nouveau_solde=nouveau
    )

    session.add(agent)
    session.add(log) # On enregistre les deux en même temps !
    session.commit()
    return agent


def create_new_profile(session: Session, profile_data: Profile) -> Profile:
    # 1. On crée le profil
    session.add(profile_data)

    # 2. On crée manuellement le log de l'événement
    nouveau_log = LogActivite(
        agent_id=profile_data.id,
        action="CREATION_COMPTE",
        nouveau_solde=profile_data.solde_courant,
    )
    session.add(nouveau_log)

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
