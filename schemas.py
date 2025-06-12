from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import List, Optional
from enum import Enum

class GenreEnum(str, Enum):
    tragedy = "Tragedy"
    comedy = "Comedy"
    drama = "Drama"
    romance = "Romance"
    fantasy = "Fantasy"
    musical = "Musical"

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

class PlayBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    genre: Optional[GenreEnum] = None
    duration_minutes: Optional[int] = Field(gt=0, le=300)
    description: Optional[str] = Field(None, max_length=500)
    release_date: date

class PlayCreate(PlayBase):
    pass

class PlayResponse(PlayBase):
    play_id: int
    class Config:
        from_attributes = True

class PlayUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    genre: Optional[GenreEnum] = None
    duration_minutes: Optional[int] = Field(None, gt=0, le=300)
    description: Optional[str] = Field(None, max_length=500)
    release_date: Optional[date] = None

class ActorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = None
    bio: Optional[str] = Field(None, max_length=500)

class ActorCreate(ActorBase):
    pass

class ActorResponse(ActorBase):
    actor_id: int
    class Config:
        from_attributes = True

class ActorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    birth_date: Optional[date] = None
    bio: Optional[str] = Field(None, max_length=500)

class DirectorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = None
    bio: Optional[str] = Field(None, max_length=500)

class DirectorCreate(DirectorBase):
    pass

class DirectorResponse(DirectorBase):
    director_id: int
    class Config:
        from_attributes = True

class DirectorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    birth_date: Optional[date] = None
    bio: Optional[str] = Field(None, max_length=500)


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-]{7,15}$")

class CustomerCreate(CustomerBase):
    password: str = Field(..., min_length=8)

class CustomerResponse(CustomerBase):
    customer_id: int
    role: UserRole = UserRole.customer
    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-]{7,15}$")
    password: Optional[str] = Field(None, min_length=8)

class ShowtimeBase(BaseModel):
    play_id: int
    start_time: datetime
    end_time: datetime
    theater_hall: str = Field(..., max_length=50)

class ShowtimeCreate(ShowtimeBase):
    pass

class ShowtimeResponse(ShowtimeBase):
    showtime_id: int
    class Config:
        from_attributes = True

class ShowtimeUpdate(BaseModel):
    play_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    theater_hall: Optional[str] = Field(None, max_length=50)

class TicketBase(BaseModel):
    showtime_id: int
    customer_id: int
    seat_number: str = Field(..., pattern=r"^[A-Z]\d{1,3}$")
    price: float = Field(..., gt=0)

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    ticket_id: int
    booking_time: datetime
    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    showtime_id: Optional[int] = None
    customer_id: Optional[int] = None
    seat_number: Optional[str] = Field(None, pattern=r"^[A-Z]\d{1,3}$")
    price: Optional[float] = Field(None, gt=0)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PlayWithRelations(PlayResponse):
    actors: List[ActorResponse] = []
    directors: List[DirectorResponse] = []

class ShowtimeWithPlay(ShowtimeResponse):
    play: PlayResponse

class TicketWithRelations(TicketResponse):
    showtime: ShowtimeResponse
    customer: CustomerResponse