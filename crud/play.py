from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import List, Optional
from models import Play
from schemas import PlayCreate, PlayUpdate
import logging

logger = logging.getLogger(_name_)


def create_play(db: Session, play: PlayCreate) -> Play:
    try:
        db_play = Play(
            title=play.title,
            genre=play.genre,
            duration_minutes=play.duration_minutes,
            description=play.description,
            release_date=play.release_date
        )

        db.add(db_play)
        db.commit()
        db.refresh(db_play)

        logger.info(f"Created new play: ID={db_play.play_id}, Title={db_play.title}")
        return db_play

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating play '{play.title}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating play: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create play"
        )


def get_play(db: Session, play_id: int) -> Optional[Play]:
    try:
        return db.query(Play).filter(Play.play_id == play_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching play ID {play_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


def get_plays(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        genre: Optional[str] = None,
        director_id: Optional[int] = None
) -> List[Play]:
    try:
        query = db.query(Play)
        if genre:
            query = query.filter(Play.genre.ilike(f"%{genre}%"))

        if director_id:
            query = query.filter(Play.directors.any(director_id=director_id))
        return query.offset(skip).limit(limit).all()

    except SQLAlchemyError as e:
        logger.error(f"Error fetching plays: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


def update_play(db: Session, play_id: int, play: PlayUpdate) -> Optional[Play]:
    try:
        db_play = get_play(db, play_id)
        if not db_play:
            logger.warning(f"Update failed: Play ID {play_id} not found")
            return None

        update_data = play.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_play, field, value)


        db.commit()
        db.refresh(db_play)

        logger.info(f"Updated play ID {play_id}")
        return db_play

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating play ID {play_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


def delete_play(db: Session, play_id: int) -> bool:
    try:
        db_play = get_play(db, play_id)
        if not db_play:
            logger.warning(f"Delete failed: Play ID {play_id} not found")
            return False

        db.delete(db_play)
        db.commit()
        logger.info(f"Deleted play ID {play_id}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting play ID {play_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


def add_director_to_play(db: Session, play_id: int, director_id: int) -> bool:
    """
    Associate a director with a play (many-to-many relationship)
    """
    try:
        play = get_play(db, play_id)
        if not play:
            logger.warning(f"Add director failed: Play ID {play_id} not found")
            return False

        if any(d.director_id == director_id for d in play.directors):
            logger.info(f"Director {director_id} already associated with play {play_id}")
            return True

        play.directors.append(director_id)
        db.commit()
        logger.info(f"Added director {director_id} to play {play_id}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error adding director to play: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


def remove_director_from_play(db: Session, play_id: int, director_id: int) -> bool:
    try:
        play = get_play(db, play_id)
        if not play:
            logger.warning(f"Remove director failed: Play ID {play_id} not found")
            return False

        initial_count = len(play.directors)
        play.directors = [d for d in play.directors if d.director_id != director_id]

        if len(play.directors) == initial_count:
            logger.info(f"Director {director_id} not associated with play {play_id}")
            return False

        db.commit()
        logger.info(f"Removed director {director_id} from play {play_id}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error removing director from play: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
