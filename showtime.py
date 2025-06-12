from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..crud import showtime as crud_showtime
from ..schemas import ShowtimeCreate, ShowtimeUpdate, ShowtimeResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED)
def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    return crud_showtime.create_showtime(db=db, showtime=showtime)

@router.get("/{showtime_id}", response_model=ShowtimeResponse)
def read_showtime(showtime_id: int, db: Session = Depends(get_db)):
    db_showtime = crud_showtime.get_showtime(db, showtime_id=showtime_id)
    if not db_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )
    return db_showtime

@router.get("/", response_model=list[ShowtimeResponse])
def list_showtimes(
    skip: int = 0,
    limit: int = 100,
    play_id: int = None,
    start_time_from: datetime = None,
    start_time_to: datetime = None,
    db: Session = Depends(get_db)
):
    return crud_showtime.get_showtimes(
        db,
        skip=skip,
        limit=limit,
        play_id=play_id,
        start_time_from=start_time_from,
        start_time_to=start_time_to
    )

@router.put("/{showtime_id}", response_model=ShowtimeResponse)
def update_showtime(
    showtime_id: int,
    showtime: ShowtimeUpdate,
    db: Session = Depends(get_db)
):
    updated_showtime = crud_showtime.update_showtime(db, showtime_id=showtime_id, showtime=showtime)
    if not updated_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )
    return updated_showtime

@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_showtime(showtime_id: int, db: Session = Depends(get_db)):
    if not crud_showtime.delete_showtime(db, showtime_id=showtime_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )