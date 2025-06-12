from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import actor as crud_actor
from ..schemas import ActorCreate, ActorUpdate, ActorResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=ActorResponse, status_code=status.HTTP_201_CREATED)
def create_actor(actor: ActorCreate, db: Session = Depends(get_db)):
    return crud_actor.create_actor(db=db, actor=actor)

@router.get("/{actor_id}", response_model=ActorResponse)
def read_actor(actor_id: int, db: Session = Depends(get_db)):
    db_actor = crud_actor.get_actor(db, actor_id=actor_id)
    if not db_actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )
    return db_actor

@router.get("/", response_model=list[ActorResponse])
def list_actors(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    db: Session = Depends(get_db)
):
    return crud_actor.get_actors(db, skip=skip, limit=limit, name=name)

@router.put("/{actor_id}", response_model=ActorResponse)
def update_actor(
    actor_id: int,
    actor: ActorUpdate,
    db: Session = Depends(get_db)
):
    updated_actor = crud_actor.update_actor(db, actor_id=actor_id, actor=actor)
    if not updated_actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )
    return updated_actor

@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    if not crud_actor.delete_actor(db, actor_id=actor_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )