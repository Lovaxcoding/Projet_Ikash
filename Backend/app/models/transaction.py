from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Relationship
from typing import Optional, TYPE_CHECKING


from .enums import OperatorType, TransactionType, TransactionStatus

if TYPE_CHECKING:
    from .profile import Profile

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id_transaction: Optional[UUID] = Field(default=None, primary_key=True)
    horodatage: datetime = Field(default_factory=datetime.utcnow)

    operateur: OperatorType
    type: TransactionType
    montant: float
    statut: TransactionStatus = Field(default=TransactionStatus.REUSSI)

    bonus: float = Field(default=0)
    numero_client: Optional[str] = None
    reference: str = Field(unique=True, index=True)
    est_saisie_manuelle: bool = Field(default=True)

    agent_id: UUID = Field(foreign_key="profiles.id")
    agent: Optional["Profile"] = Relationship(back_populates="agent_transactions")
