from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import customer as crud_customer
from ..schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud_customer.create_customer(db=db, customer=customer)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer

@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    return crud_customer.get_customers(
        db,
        skip=skip,
        limit=limit,
        name=name,
        email=email
    )

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    updated_customer = crud_customer.update_customer(db, customer_id=customer_id, customer=customer)
    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    if not crud_customer.delete_customer(db, customer_id=customer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )