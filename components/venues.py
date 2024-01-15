# app/venues.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, insert, update, delete
from .authentication import oauth2_scheme, create_access_token
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from .models import VenueCreate, venue_table, images_table, VenueResponse, VenueCreate, VenueUpdate, VenueDelete, VenueLocationResponse, venue_table, forecastData
from .authentication import get_logged_in_user
from .database import get_database
from fastapi import Body
from urllib.parse import urlparse
from geopy.geocoders import Nominatim
from unshortenit import UnshortenIt
from urllib.parse import urlparse, parse_qs
import base64
from bs4 import BeautifulSoup

from ApiAuth.authentication import hash_password, create_access_token, verify_password, get_current_user
from ApiAuth.database import get_db, User

router = APIRouter()

import logging

@router.post("/createVenue", response_model=dict)
async def create_venue(
    venue_data: VenueCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Logging statement to print information about the received request
        logging.info(f"Received request from {current_user['sub']}")
        logging.info(f"Request data: {venue_data.dict()}")

        # Ensure that the owner username is obtained dynamically
        venue_data_dict = venue_data.dict()

        # Insert venue data into the venue table
        query_insert_venue = insert(venue_table).values(
            ownerusername=venue_data_dict["ownerusername"],
            ownername=venue_data_dict["ownername"],
            phonenumber=venue_data_dict["phonenumber"],
            city=venue_data_dict["city"],
            country=venue_data_dict["country"],
            location=venue_data_dict["location"],
            workingdays=venue_data_dict["workingdays"],
            price=venue_data_dict["price"],
            capacity=venue_data_dict["capacity"],
            area=venue_data_dict["area"],
            ground=venue_data_dict["ground"],
            description=venue_data_dict["description"],
        )
        venue_id = await db.execute(query_insert_venue) 

        # Insert image URLs into the images table
        for i, image_url in enumerate(venue_data.images):
            query_insert_image = insert(images_table).values(
                ownerusername=venue_data_dict["ownerusername"],
                location=venue_data_dict["location"],
                image_name=f"Image {i + 1}",
                image_url=image_url,
            )
            await db.execute(query_insert_image)

        return {"message": "Venue created successfully"}
    except Exception as e:
        # Log the error or return a more informative response
        error_detail = {"detail": f"Error creating venue: {str(e)}"}
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_detail,
        )
        
from fastapi import HTTPException

@router.options("/createVenue")
async def options_create_venue():
    return {"msg": "OK"}

# Endpoint to get venues for the current user
@router.get("/getVenuesForCurrentOwner", response_model=List[VenueCreate])
async def get_venues_for_user(
    currentUser: dict = Depends(get_current_user),
    current_user: dict = Depends(get_logged_in_user),
    db=Depends(get_database) 
    ):
    try:
        # Fetch venues based on the current user's ownerusername
        query_venues = select([venue_table]).where(venue_table.c.ownerusername == current_user['username'])
        venues = await db.fetch_all(query_venues)
        
        # Convert venues to a list of dictionaries
        venues_list = [dict(venue) for venue in venues]
        
        # Fetch images for each venue
        for venue in venues_list:
            query_images = select([images_table.c.image_url]).where(
                (images_table.c.location == venue['location']) &
                (images_table.c.ownerusername == venue['ownerusername'])
            )
            images = await db.fetch_all(query_images)
            venue['images'] = [image['image_url'] for image in images]
            
        print('Venues sent to client:', venues_list)
        return venues_list
    except Exception as e:
        print(f"Error fetching venues: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

# Update /getVenues endpoint to use the modified VenueResponse model
@router.get("/getVenues", response_model=List[VenueResponse])
async def get_all_venues(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Fetch all venues
        query_venues = select([venue_table])
        venues = await db.fetch_all(query_venues)

        # Fetch images for each venue
        venues_list = []
        for venue in venues:
            venue_dict = dict(venue)
            query_images = select([images_table.c.image_url]).where(
                (images_table.c.location == venue_dict['location']) &
                (images_table.c.ownerusername == venue_dict['ownerusername'])
            )
            images = await db.fetch_all(query_images)
            venue_dict['images'] = [image['image_url'] for image in images]
            venues_list.append(venue_dict)

        # Ensure that the 'images' attribute is always a list
        for venue in venues_list:
            venue['images'] = venue.get('images', [])

        # Convert the list of dictionaries to VenueResponse objects
        venues_response = [VenueResponse(**{key: venue[key] for key in VenueResponse.__annotations__}) for venue in venues_list]

        print('Venues sent to client:', venues_response)
        return venues_response
    except Exception as e:
        print(f"Error fetching venues: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


from fastapi import Query


# Create a new endpoint for filtered venues
@router.get("/getFilteredVenues", response_model=List[VenueResponse])
async def get_filtered_venues(
    city: str = Query(None, description="Filter by city"),
    country: str = Query(None, description="Filter by country"),
    pitch_type: str = Query(None, description="Filter by pitch type"),
    price_range: int = Query(None, description="Filter by price range"),
    capacity_range: int = Query(None, description="Filter by capacity range"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    try:
        # Start building the base query
        query_venues = select([venue_table])

        # Apply filters based on query parameters
        if city:
            query_venues = query_venues.where(venue_table.c.city == city)

        if country:
            query_venues = query_venues.where(venue_table.c.country == country)

        if pitch_type:
            query_venues = query_venues.where(venue_table.c.ground == pitch_type)

        # Apply filters for price range if provided
        if price_range is not None:
            query_venues = query_venues.where(venue_table.c.price <= price_range)

        # Apply filters for capacity range if provided
        if capacity_range is not None:
            query_venues = query_venues.where(venue_table.c.capacity <= capacity_range)

        # Fetch filtered venues
        venues = await db.fetch_all(query_venues)

        # Fetch images for each venue
        venues_list = []
        for venue in venues:
            venue_dict = dict(venue)
            query_images = select([images_table.c.image_url]).where(
                (images_table.c.location == venue_dict['location']) &
                (images_table.c.ownerusername == venue_dict['ownerusername'])
            )
            images = await db.fetch_all(query_images)
            venue_dict['images'] = [image['image_url'] for image in images]
            venues_list.append(venue_dict)

        # Ensure that the 'images' attribute is always a list
        for venue in venues_list:
            venue['images'] = venue.get('images', [])

        # Convert the list of dictionaries to VenueResponse objects
        venues_response = [VenueResponse(**{key: venue[key] for key in VenueResponse.__annotations__}) for venue in venues_list]

        print('Filtered venues sent to the client:', venues_response)
        return venues_response
    except Exception as e:
        print(f"Error fetching filtered venues: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@router.put("/updateVenue", response_model=dict)
async def update_venue(
    venue_data: VenueUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    try:
        # Check if the venue belongs to the current owner
        query_check_ownership = select([venue_table.c.ownerusername]).where(
            (venue_table.c.location == venue_data.location) & (venue_table.c.ownerusername == venue_data.ownerusername)
        )
        owner_username = await db.execute(query_check_ownership)

        if not owner_username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this venue.",
            )

        # Convert Pydantic model to dictionary and filter out unset values
        update_data = venue_data.model_dump(exclude_unset=True)

        # Extract images from update_data
        images = update_data.pop("images", None)

        # Update venue data in the database
        if update_data:
            query_update_venue = (
                update(venue_table)
                .where(venue_table.c.location == venue_data.location)
                .values(**update_data)
            )
            await db.execute(query_update_venue)

        # Handle image updates separately
        if images:
            # First, delete existing images for the venue
            delete_query = images_table.delete().where(
                (images_table.c.location == venue_data.location) &
                (images_table.c.ownerusername == venue_data.ownerusername)
            )
            await db.execute(delete_query)

            # Insert new images for the venue
            for i, image_url in enumerate(images):
                insert_query = insert(images_table).values(
                    ownerusername=venue_data.ownerusername,
                    location=venue_data.location,
                    image_name=f"Image {i + 1}",
                    image_url=image_url,
                )
                await db.execute(insert_query)

        return {"message": "Venue updated successfully"}
    except Exception as e:
        import traceback
        print(f"Error updating venue: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )




@router.delete("/deleteVenue", response_model=dict)
async def delete_venue(
    venue_data: VenueDelete,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Check if the venue belongs to the current owner
        query_check_ownership = select([venue_table.c.ownerusername]).where(
            (venue_table.c.location == venue_data.location) & (venue_table.c.ownerusername == venue_data.ownerusername)
        )
        owner_username = await db.execute(query_check_ownership)
        if not owner_username:
            raise HTTPException(
                status_code=403,
                detail="You are not the owner of this venue.",
            )

        # Delete images associated with the venue
        delete_images_query = images_table.delete().where(
            (images_table.c.location == venue_data.location) &
            (images_table.c.ownerusername == venue_data.ownerusername)
        )
        await db.execute(delete_images_query)

        # Delete the venue record
        delete_venue_query = venue_table.delete().where(
            (venue_table.c.location == venue_data.location) &
            (venue_table.c.ownerusername == venue_data.ownerusername)
        )
        await db.execute(delete_venue_query)

        return {"message": "Venue deleted successfully"}
    except Exception as e:
        print(f"Error deleting venue: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )



geolocator = Nominatim(user_agent="teamup")
unshortenit = UnshortenIt()

import requests
from urllib.parse import unquote

@router.get("/get_all_venues_locations", response_model=List[VenueLocationResponse])
async def get_all_venues_locations(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    """
    Endpoint to retrieve map data for all venues using direct extraction from Google Maps share links.
    """
    query_venues = select([venue_table])
    venues = await db.fetch_all(query_venues)

    locations_data = []

    for venue in venues:
        # Extract the location from the Google Maps link
        location_url = venue['location']

        try:
            # Unshorten the URL
            full_url = unshortenit.unshorten(location_url)
            print(f"Unshortened URL: {full_url}")

            # Use web scraping to extract location data
            location_data = extract_location_data(full_url)
            print(f"Location Data: {location_data}")

            locations_data.append(location_data)

        except Exception as e:
            print(f"Error processing location URL: {location_url}, Error: {e}")

    return locations_data

def extract_location_data(google_maps_url):
    # Parse Google Maps URL to get path and query parameters
    parsed_url = urlparse(google_maps_url)
    path_segments = parsed_url.path.split('/')
    
    encoded_name = path_segments[3]
    name = unquote(encoded_name)
    name = name.replace("+", " ")


    # Extract latitude and longitude from the '@' parameter in the query string
    coordinates = path_segments[4] if len(path_segments) > 2 else ''
    lat = coordinates[1:coordinates.index(",")]
    lng = coordinates[coordinates.index(",")+1:coordinates.rindex(",")]

    location_data = {
        "name" : name if name else None,
        "latitude": (lat) if lat else None,
        "longitude": (lng) if lng else None,
    }

    return location_data



'''@router.get("/get_weather_forecast")
async def get_weather_forecast(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    date: str = Query(..., description="Date in the format YYYY-MM-DD"),
    api_key: str = Query(..., description="OpenWeatherMap API key"),
):
    try:
        # Convert date to timestamp
        timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())

        # Make request to OpenWeatherMap API
        base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
        params = {
            "lat": latitude,
            "lon": longitude,
            "dt": timestamp,
            "appid": api_key,
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()

        weather_data = response.json()

        return weather_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")'''
    
import requests
from .Keys import openWeatherMapAPIKey


@router.get("/get_weather_forecast")
async def get_weather_forecast(
  forecastData: forecastData,
  current_user: dict = Depends(get_current_user),
  db=Depends(get_database),
):
    try:
        # Convert the URL to a string
        full_url = unshortenit.unshorten(str(forecastData.googleMapsUrl))
        print(f"Unshortened URL: {full_url}")

        # Check if the URL is unshortened successfully
        if not full_url:
            raise HTTPException(status_code=400, detail="Unable to unshorten the provided URL")

        location_data = extract_location_data(full_url)

        # Now we make the request to OpenWeatherMap API
        base_url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": location_data.get("latitude"), 
            "lon": location_data.get("longitude"),
            "appid": openWeatherMapAPIKey,
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()

        weather_data = response.json()

        return weather_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")

'''from .Keys import mapTilerAPIKey
from fastapi.responses import HTMLResponse
import maptiler


# Define the endpoint to create a map view for venues
@router.get("/map_view", response_class=HTMLResponse)
async def map_view():
    # Query all venues from the database
    query = select([venue_table])
    venues_data = await database.fetch_all(query)

    # Check if 'container' is being correctly substituted
    try:
        html_content = f"""<html>
            <head>
                <script src="https://api.maptiler.com/maps/streets/style.json?key={mapTilerAPIKey}"></script>
            </head>
            <body>
                <div id="map" style="height: 1200px;"></div>
                <script>
                    const map = new maptiler.Map({{
                        container: 'map', 
                        style: maptilersdk.MapStyle.STREETS,
                        center: [12.550343, 55.665957],
                        zoom: 9,
                    }});
                    
                    // Add markers for each venue
                    {generate_markers_js(venues_data)}
                </script>
            </body>
        </html>"""
    except KeyError as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

    return HTMLResponse(content=html_content, status_code=200)

# Helper function to generate JavaScript code for markers
def generate_markers_js(venues_data):
    markers_js = ""
    for venue in venues_data:
        location_url = venue["location"]
        
        full_url = unshortenit.unshorten(location_url)
        location_data = extract_location_data(full_url)
        
        markers_js += """new maptilersdk.Marker()
            .setLngLat([{}, {}])
            .addTo(map);""".format(location_data["latitude"], location_data["longitude"])
    return markers_js '''

