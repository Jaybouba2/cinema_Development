from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Director
from schemas import DirectorCreate, DirectorUpdate
import logging

logger = logging.getLogger(_name_)

def create_director(db: Session, director: DirectorCreate) -> Director:
    try:
        db_director = Director(**director.model_dump())
        db.add(db_director)
        db.commit()
        db.refresh(db_director)
        logger.info(f"Created director ID={db_director.director_id}")
        return db_director
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating director: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


def get_director(db: Session, director_id: int) -> Director:
    director = db.query(Director).filter(Director.director_id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director


def get_directors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Director).offset(skip).limit(limit).all()


def update_director(db: Session, director_id: int, update_data: DirectorUpdate) -> Director:
    director = get_director(db, director_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(director, field, value)
    db.commit()
    db.refresh(director)
    return director


def delete_director(db: Session, director_id: int) -> bool:
    director = get_director(db, director_id)
    db.delete(director)
    db.commit()
    return True
