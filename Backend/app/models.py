from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# Modèle pour les transactions financières
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    montant: float
    type_op: str  # 'DEPOT', 'RETRAIT', 'TRANSFERT'
    reference_sms: str = Field(unique=True) # Pour éviter les doublons
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str