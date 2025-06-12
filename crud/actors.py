from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Actor
from schemas import ActorCreate, ActorUpdate
import logging

logger = logging.getLogger(_name_)

def create_actor(db: Session, actor: ActorCreate) -> Actor:
    try:
        db_actor = Actor(**actor.model_dump())
        db.add(db_actor)
        db.commit()
        db.refresh(db_actor)
        logger.info(f"Created actor ID={db_actor.actor_id}")
        return db_actor
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


def get_actor(db: Session, actor_id: int) -> Actor:
    actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


def get_actors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Actor).offset(skip).limit(limit).all()


def update_actor(db: Session, actor_id: int, update_data: ActorUpdate) -> Actor:
    actor = get_actor(db, actor_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(actor, field, value)
    db.commit()
    db.refresh(actor)
    return actor


def delete_actor(db: Session, actor_id: int) -> bool:
    actor = get_actor(db, actor_id)
    db.delete(actor)
    db.commit()
    return True
