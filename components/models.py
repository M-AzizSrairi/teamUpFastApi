# fastapi/models.py
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Union
from sqlalchemy import Column, String, DateTime, MetaData, Table, func, ForeignKey, Integer, LargeBinary, Text, Enum
from sqlalchemy.types import Float, Date, Time, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, time, datetime


metadata = MetaData()

class UserRegistration(BaseModel):
    email: str
    username: str
    password: str
    confirm_password: str
    dob: date
    city: str
    user_type: str

class RegistrationResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class VenueCreate(BaseModel):
    ownerusername: str
    ownername: str
    phonenumber: str
    city: str
    country: str
    location: str
    workingdays: str
    price: int
    capacity: int
    area: str
    ground: str
    description: str
    images: List[str]
    
    
class VenueResponse(BaseModel):
    ownerusername: str
    ownername: str
    phonenumber: str
    city: str
    country: str
    location: str
    workingdays: str
    price: int
    capacity: int
    area: str
    ground: str
    description: str
    images: List[str]
    
    
class VenueUpdate(BaseModel):
    ownerusername: Optional[str] = None
    ownername: Optional[str] = None
    phonenumber: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    location: Optional[str] = None
    workingdays: Optional[str] = None
    price: Optional[int] = None
    capacity: Optional[int] = None
    area: Optional[str] = None
    ground: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None


class VenueDelete(BaseModel):
    location: str
    ownerusername: str
    
class BookingCreate(BaseModel):
    playerusername: str
    location: str
    bookingdate: date
    starttime: time
    endtime: time
    numberofpeople: int
    
class BookingResponse(BaseModel):
    booking_id: int
    ownerusername: str
    response: str  #either "accept" or "reject"

class BookingResponse(BaseModel):
    bookingid: int
    playerusername: str
    location: str
    bookingdate: date
    starttime: time
    endtime: time
    numberofpeople: int
    status: str
    createdat: datetime

    class Config:
        arbitrary_types_allowed = True

class OwnerBookingsResponse(BaseModel):
    owner_bookings: List[BookingResponse]

class PlayerBookingResponse(BaseModel):
    bookingid: int
    ownerusername: str
    location: str
    bookingdate: date
    starttime: time
    endtime: time
    numberofpeople: int
    status: str
    createdat: datetime

    class Config:
        arbitrary_types_allowed = True

class PlayerBookingsResponse(BaseModel):
    Player_bookings: List[PlayerBookingResponse]
    
class TeamCreate(BaseModel):
    captainid : str
    teamname: str

class PlayerProfile(BaseModel):
    username: str
    age: int
    city: str

class TeamResponse(BaseModel):
    teamid: int
    teamname: str
    createdat: datetime
    captainid: str

class InvitationCreate(BaseModel):
    invitedplayerid: str
    invitedby: str

class InvitationResponse(BaseModel):
    invitationid: int
    teamid: int
    invitedplayerid: str
    invitedby: str
    invitedat: Optional[datetime]
    status: Optional[str]

# Pydantic model for response
class VenueLocationResponse(BaseModel):
    name: str
    latitude: str
    longitude: str
    
# Pydantic model for venue data weather forescast
class forecastData(BaseModel):
    googleMapsUrl : str 
    

    
    


# SQLAlchemy model for the Player table
player_table = Table(
    "player",
    metadata,
    Column("email", String, unique=True, index=True),
    Column("username", String, index=True),
    Column("password", String),
    Column("dob", DateTime(timezone=True), server_default=func.now()),
    Column("city", String),
    Column("user_type", String),
)

# SQLAlchemy model for the Owner table
owner_table = Table(
    "owner",
    metadata,
    Column("email", String, unique=True, index=True),
    Column("username", String, index=True),
    Column("password", String),
    Column("dob", DateTime(timezone=True), server_default=func.now()),
    Column("city", String),
    Column("user_type", String),
)

# SQLAlchemy model for the Venue table
venue_table = Table(
    "venue",
    metadata,
    Column("ownerusername", String, ForeignKey("owner.username", ondelete="CASCADE")),
    Column("ownername", String),
    Column("phonenumber", String),
    Column("city", String),
    Column("country", String),
    Column("location", String, primary_key=True),
    Column("workingdays", String),
    Column("price", Integer),
    Column("capacity", Integer),
    Column("area", String),
    Column("ground", String),
    Column("description", String), 
    Column("reviews", Float),
    Column("numberoftimeschecked", Integer),
    Column("numberoftimesbooked", Integer),
    Column("availability", String, default='yes'),
)

# SQLAlchemy model for the Venue table
images_table = Table(
    "images",
    metadata,
    Column("image_id", Integer, primary_key=True),
    Column("ownerusername", String, ForeignKey("venues.ownerusername")),
    Column("location", String, ForeignKey("venues.location")),
    Column("image_name", String),
    Column("image_url", String),
)

booking = Table(
    "booking",
    metadata,
    Column("bookingid", Integer, primary_key=True, index=True),
    Column("playerusername", String, ForeignKey("player.username"), nullable=False),
    Column("ownerusername",String, ForeignKey("owner.username"), nullable=False),
    Column("location",String, ForeignKey("venue.location"), nullable=False),
    Column("bookingdate",Date , nullable=False),
    Column("starttime",Time, nullable=False),
    Column("endtime",Time, nullable=False),
    Column("numberofpeople", Integer, nullable=False),
    Column("status", String(20), server_default="pending"),
    Column("createdat", TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False),
)

team = Table(
    "team",
    metadata,
    Column("teamid", Integer, primary_key=True, index=True),
    Column("teamname", String, index=True),
    Column("createdat", TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False),
    Column("captainid", String, ForeignKey('player.username')),
)


teammembership = Table(
    "teammembership",
    metadata,
    Column("teamid", Integer, ForeignKey('team.teamid'), primary_key=True),
    Column("playerid", String, ForeignKey('player.username'), primary_key=True),
    Column("joined_at", TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False),
)


invitation = Table(
    "invitation",
    metadata,
    Column("invitationid", Integer, primary_key=True, index=True),
    Column("teamid", Integer, ForeignKey('team.teamid')),
    Column("invitedplayerid", String, ForeignKey('player.username')),
    Column("invitedat", TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False),
    Column("status", Enum('pending', 'accepted', 'rejected'), default='pending'),
    Column("invitedby", String, ForeignKey('player.username')),
    Column("responded_at", TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False),
)

