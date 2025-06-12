from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from database import get_db
from crud import play as crud_play

router = APIRouter()

@router.post('/', response_model=schemas.Play)
def create_play_endpoint(
    play: schemas.PlayCreate,
    db: Session = Depends(get_db)
):
    return crud_play.create_play(db=db, play=play)

@router.get('/{play_id}', response_model=schemas.Play)
def read_play(play_id: int, db: Session = Depends(get_db)):
    play = crud_play.get_play(db, play_id=play_id)
    if not play:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Play not found'
        )
    return play

@router.get('/', response_model=list[schemas.Play])
def read_plays(
    skip: int = 0,
    limit: int = 100,
    genre: str = None,
    db: Session = Depends(get_db)
):
    return crud_play.get_plays(
        db,
        skip=skip,
        limit=limit,
        genre=genre
    )
