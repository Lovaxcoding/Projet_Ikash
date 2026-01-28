from sqlmodel import Session, select
from app.models import Transaction


def create_transaction(session: Session, transaction_data: Transaction):
    session.add(transaction_data)
    session.commit()
    session.refresh(transaction_data)
    return transaction_data


def get_all_transactions(session: Session):
    statement = select(Transaction)
    return session.exec(statement).all()
