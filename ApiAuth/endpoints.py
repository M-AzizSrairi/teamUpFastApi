# ApiAuth/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, SessionLocal, UserCreate, User, UserLogin
from pydantic import BaseModel
from .authentication import hash_password, create_access_token, verify_password, get_current_user


router = APIRouter()

@router.post("/registerApiUser", response_model=dict)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = db.query(User).filter(User.email == user_create.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing it
    hashed_password = hash_password(user_create.password)

    # Save the user to the database
    db_user = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully"}

@router.post("/loginApiUser", response_model=dict)
async def login_user(
    UserLogin: UserLogin,
    db: Session = Depends(get_db)
    ):
    # Check if the user exists
    user = db.query(User).filter(User.username == UserLogin.username).first()
    if not user or not verify_password(UserLogin.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate an access token
    access_token = create_access_token({"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


class UserProfile(BaseModel):
    id: int
    username: str
    email: str

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(id=user.id, username=user.username, email=user.email)
