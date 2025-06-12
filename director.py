from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import director as crud_director
from ..schemas import DirectorCreate, DirectorUpdate, DirectorResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    return crud_director.create_director(db=db, director=director)

@router.get("/{director_id}", response_model=DirectorResponse)
def read_director(director_id: int, db: Session = Depends(get_db)):
    db_director = crud_director.get_director(db, director_id=director_id)
    if not db_director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )
    return db_director

@router.get("/", response_model=list[DirectorResponse])
def list_directors(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    db: Session = Depends(get_db)
):
    return crud_director.get_directors(db, skip=skip, limit=limit, name=name)

@router.put("/{director_id}", response_model=DirectorResponse)
def update_director(
    director_id: int,
    director: DirectorUpdate,
    db: Session = Depends(get_db)
):
    updated_director = crud_director.update_director(db, director_id=director_id, director=director)
    if not updated_director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )
    return updated_director

@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    if not crud_director.delete_director(db, director_id=director_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )