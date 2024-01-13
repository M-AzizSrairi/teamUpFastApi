# main.py
import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, Form, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sqlalchemy import MetaData
from components.authentication import router as auth_router
from components.database import database
from components.venues import router as venue_router
from components.booking import router as booking_router
from components.teams import router as team_router
from dotenv import load_dotenv
import os

app = FastAPI()


app.include_router(auth_router)
app.include_router(venue_router)
app.include_router(booking_router)
app.include_router(team_router)

metadata = MetaData()

# CORS middleware configuration
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handler to connect to the database when the app starts
@app.on_event("startup")
async def startup():
    await database.connect()

# Event handler to disconnect from the database when the app shuts down
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Event handler to connect to the database when the app starts
@app.on_event("startup")
async def startup():
    await database.connect()

# Event handler to disconnect from the database when the app shuts down
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    # Get API keys from environment variables or use default values
    open_weather_map_api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

    # Pass the API keys to your components
    venue_router.openapi_dependencies = [Depends(open_weather_map_api_key)]

    uvicorn.run("app.api:app", host="127.0.0.1", port=8001, reload=True)
