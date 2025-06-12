from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import ticket as crud_ticket
from ..schemas import TicketCreate, TicketUpdate, TicketResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return crud_ticket.create_ticket(db=db, ticket=ticket)

@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud_ticket.get_ticket(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return db_ticket

@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    skip: int = 0,
    limit: int = 100,
    showtime_id: int = None,
    customer_id: int = None,
    db: Session = Depends(get_db)
):
    return crud_ticket.get_tickets(
        db,
        skip=skip,
        limit=limit,
        showtime_id=showtime_id,
        customer_id=customer_id
    )

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = crud_ticket.update_ticket(db, ticket_id=ticket_id, ticket=ticket)
    if not updated_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return updated_ticket

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    if not crud_ticket.delete_ticket(db, ticket_id=ticket_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
