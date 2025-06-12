from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Showtime
from schemas import ShowtimeCreate, ShowtimeUpdate
import logging

logger = logging.getLogger(_name_)

def create_showtime(db: Session, showtime: ShowtimeCreate) -> Showtime:
    try:
        db_showtime = Showtime(**showtime.model_dump())
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)
        logger.info(f"Created showtime ID={db_showtime.showtime_id}")
        return db_showtime
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating showtime: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


def get_showtime(db: Session, showtime_id: int) -> Showtime:
    showtime = db.query(Showtime).filter(Showtime.showtime_id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime


def get_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Showtime).offset(skip).limit(limit).all()


def update_showtime(db: Session, showtime_id: int, update_data: ShowtimeUpdate) -> Showtime:
    showtime = get_showtime(db, showtime_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(showtime, field, value)
    db.commit()
    db.refresh(showtime)
    return showtime


def delete_showtime(db: Session, showtime_id: int) -> bool:
    showtime = get_showtime(db, showtime_id)
    db.delete(showtime)
    db.commit()
    return True
