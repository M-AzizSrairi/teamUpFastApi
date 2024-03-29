# app/authentication.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from databases import Database
from datetime import datetime, timedelta
from sqlalchemy.sql import select, insert
from pydantic import BaseModel
import secrets
from  .models import RegistrationResponse, UserRegistration, player_table, owner_table
from sqlalchemy.orm import Session 

from components.database import database
from databases import Database 
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from .database import get_database
from ApiAuth.authentication import get_current_user

router = APIRouter()


# Endpoint for user registration
@router.post("/register", response_model=RegistrationResponse)
async def register( user_data: UserRegistration,db: Database=Depends(get_database)):
    try:
        #Validation of password matching
        if user_data.password != user_data.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Determine the table based on user_type
        table = player_table if user_data.user_type == "player" else owner_table

        # Check if email or username already exists
        query_existing_user = select([table]).where(
            (table.c.email == user_data.email) | (table.c.username == user_data.username)
        )
        existing_user = await db.fetch_one(query_existing_user)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email or username already registered")
        # Hash the password before storing it
        hashed_password = bcrypt.hash(user_data.password)
        # Insert user data into the respective table
        query_insert_user = table.insert().values(
            email=user_data.email,
            username=user_data.username,
            password=hashed_password,
            dob=user_data.dob,
            city=user_data.city,
            user_type=user_data.user_type,
        )
        # Execution
        await db.execute(query_insert_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise e

import secrets

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

import logging

# Pydantic model for the token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str

# Function to create a new JWT token
def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_date = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expires_date})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Login endpoint with JWT token issuance and password hashing
@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Database=Depends(get_database),
):
    try:
        # Check if the user exists in the player table
        player_query = player_table.select().where(player_table.c.username == user_data.username)
        player_result = await db.fetch_one(player_query)

        if player_result and bcrypt.verify(user_data.password, player_result["password"]):
            token_data = {"sub": user_data.username, "userType": "player"}
            access_token = create_access_token(token_data)
            return {"access_token": access_token, "token_type": "bearer"}

        # Check if the user exists in the owner table
        owner_query = owner_table.select().where(owner_table.c.username == user_data.username)
        owner_result = await db.fetch_one(owner_query)

        if owner_result and bcrypt.verify(user_data.password, owner_result["password"]):
            token_data = {"sub": user_data.username, "userType": "owner"}
            access_token = create_access_token(token_data)
            return {"access_token": access_token, "token_type": "bearer"}

        # If user not found or password doesn't match, raise HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
def get_logged_in_user(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username=payload.get("sub")
        token_data = {"sub": username}
        print(f"Decoded Token: {jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])}")
        return token_data
