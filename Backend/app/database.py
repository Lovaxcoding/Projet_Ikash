import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from app.models.enums import RoleType, OperatorType, TransactionType, TransactionStatus
from app.models.profile import Profile
from app.models.transaction import Transaction
from app.models.log import LogActivite 


# On charge le .env qui est dans le dossier parent (backend/)
load_dotenv()
def get_session():
    with Session(engine) as session:
        yield session


DATABASE_URL = os.getenv("DATABASE_URL")

# Création de l'engine avec une configuration simple
engine = create_engine(
    DATABASE_URL, echo=True
)  # echo=True permet de voir le SQL dans le terminal


def create_db_and_tables():
    # C'est ici que la magie opère
    SQLModel.metadata.create_all(engine)
    print("Base de données et tables créées.")
