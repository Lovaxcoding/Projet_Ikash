from pydantic import BaseModel
from uuid import UUID


class SoldeUpdateRequest(BaseModel):
    agent_id: UUID
    admin_id: UUID
    montant: float
    action_description: str = "Ajustement manuel du solde"
