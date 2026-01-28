from enum import Enum


class OperatorType(str, Enum):
    TELMA = "TELMA"
    AIRTEL = "AIRTEL"
    ORANGE = "ORANGE"
    AUTRE = "AUTRE"


class TransactionType(str, Enum):
    DEPOT = "DEPOT"
    RETRAIT = "RETRAIT"
    TRANSFERT = "TRANSFERT"
    CREDIT = "CREDIT"


class TransactionStatus(str, Enum):
    REUSSI = "REUSSI"
    ECHEC = "ECHEC"
    EN_ATTENTE = "EN_ATTENTE"
    ARCHIVEE = "ARCHIVEE"

class RoleType(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"