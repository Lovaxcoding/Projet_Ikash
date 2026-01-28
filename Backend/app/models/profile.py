from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .enums import RoleType
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: UUID = Field(primary_key=True)  # Lié à l'UUID de Supabase Auth
    nom: str
    role: str = Field(default=RoleType.AGENT.value)
    code_pin: Optional[str] = None
    solde_courant: float = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # MULTI-TENANCY : Lien vers l'administrateur
    admin_id: Optional[UUID] = Field(default=None, foreign_key="profiles.id")

    # Relations (pour faciliter les requêtes)
    agent_transactions: List["Transaction"] = Relationship(back_populates="agent")
