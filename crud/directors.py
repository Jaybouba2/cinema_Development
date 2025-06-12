from sqlalchemy.orm import Session
from app import models, schemas

def get_director(db: Session, director_id: int):
    return db.query(models.Director).filter(models.Director.id == director_id).first()

def get_directors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Director).offset(skip).limit(limit).all()

def create_director(db: Session, director: schemas.DirectorCreate):
    db_director = models.Director(name=director.name, bio=director.bio)
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director
