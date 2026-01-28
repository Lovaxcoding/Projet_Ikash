from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    montant: float
    type_op: str  # ex: "RETRAIT", "DEPOT", "TRANSFERT"
    reference_sms: str = Field(unique=True, index=True)
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str