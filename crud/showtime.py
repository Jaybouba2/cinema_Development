from sqlalchemy.orm import Session
from app import models, schemas

def get_showtime(db: Session, showtime_id: int):
    return db.query(models.Showtime).filter(models.Showtime.id == showtime_id).first()

def get_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Showtime).offset(skip).limit(limit).all()

def create_showtime(db: Session, showtime: schemas.ShowtimeCreate):
    db_showtime = models.Showtime(
        play_id=showtime.play_id,
        show_date=showtime.show_date,
        location=showtime.location
    )
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime
