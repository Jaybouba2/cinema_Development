from sqlalchemy.orm import Session
from app import models, schemas

def get_actor(db: Session, actor_id: int):
    return db.query(models.Actor).filter(models.Actor.id == actor_id).first()

def get_actors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Actor).offset(skip).limit(limit).all()

def create_actor(db: Session, actor: schemas.ActorCreate):
    db_actor = models.Actor(name=actor.name, bio=actor.bio)
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor
