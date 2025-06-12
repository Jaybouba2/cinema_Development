from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Ticket
from schemas import TicketCreate, TicketUpdate
import logging

logger = logging.getLogger(_name_)

def create_ticket(db: Session, ticket: TicketCreate) -> Ticket:
    try:
        db_ticket = Ticket(**ticket.model_dump())
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        logger.info(f"Issued ticket ID={db_ticket.ticket_id}")
        return db_ticket
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


def get_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()


def update_ticket(db: Session, ticket_id: int, update_data: TicketUpdate) -> Ticket:
    ticket = get_ticket(db, ticket_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int) -> bool:
    ticket = get_ticket(db, ticket_id)
    db.delete(ticket)
    db.commit()
    return True
