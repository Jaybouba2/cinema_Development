from sqlalchemy.orm import Session
from app import models, schemas

def get_play(db: Session, play_id: int):
    return db.query(models.Play).filter(models.Play.id == play_id).first()

def get_plays(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Play).offset(skip).limit(limit).all()

def create_play(db: Session, play: schemas.PlayCreate):
    db_play = models.Play(
        title=play.title,
        description=play.description,
        duration_minutes=play.duration_minutes
    )
    db.add(db_play)
    db.commit()
    db.refresh(db_play)
    return db_play
