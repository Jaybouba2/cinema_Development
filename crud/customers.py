from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Customer
from schemas import CustomerCreate, CustomerUpdate
import logging

logger = logging.getLogger(_name_)


def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    try:
        db_customer = Customer(**customer.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Created customer ID={db_customer.customer_id}")
        return db_customer
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


def get_customer(db: Session, customer_id: int) -> Customer:
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, update_data: CustomerUpdate) -> Customer:
    customer = get_customer(db, customer_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> bool:
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()
    return True
