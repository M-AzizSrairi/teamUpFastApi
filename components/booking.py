from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from components.database import get_database
from components.models import BookingCreate, booking, venue_table, BookingResponse, RespondBookingResponse
from sqlalchemy.sql import select, insert, update, delete, and_, or_
from ApiAuth.authentication import get_current_user


router = APIRouter()

@router.post("/createBooking", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Check if the number of people does not exceed the venue capacity
        query_venue_capacity = select([venue_table.c.capacity]).where(
            venue_table.c.location == booking_data.location
        )
        venue_capacity = await db.execute(query_venue_capacity)
        
        if not venue_capacity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found",
            )

        if booking_data.numberofpeople > venue_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of people exceeds venue capacity",
            )

        # Check for overlapping bookings
        query_overlapping_bookings = select([booking.c.starttime, booking.c.endtime]).where(
            and_(
                booking.c.location == booking_data.location,
                booking.c.bookingdate == booking_data.bookingdate,
                or_(
                    and_(
                        booking.c.starttime <= booking_data.starttime,
                        booking_data.starttime <= booking.c.endtime
                    ),
                    and_(
                        booking.c.starttime <= booking_data.endtime,
                        booking_data.endtime <= booking.c.endtime
                    ),
                    and_(
                        booking.c.starttime >= booking_data.starttime,
                        booking.c.endtime <= booking_data.endtime
                    )
                )
            )
        )
        overlapping_bookings = await db.execute(query_overlapping_bookings)

        if overlapping_bookings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking time overlaps with existing bookings",
            )

        # Get owner username based on the venue location
        query_owner_username = select([venue_table.c.ownerusername]).where(
            venue_table.c.location == booking_data.location
        )
        owner_username = await db.execute(query_owner_username)

        if not owner_username:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found",
            )

        # Insert booking data into the database
        query_create_booking = insert(booking).values(
            playerusername=booking_data.playerusername,
            ownerusername=owner_username,
            location=booking_data.location,
            bookingdate=booking_data.bookingdate,
            starttime=booking_data.starttime,
            endtime=booking_data.endtime,
            numberofpeople=booking_data.numberofpeople,
        )
        await db.execute(query_create_booking)

        return {"message": "Booking created successfully"}

    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPExceptions to let FastAPI handle them

    except Exception as e:
        import traceback
        print(f"Error creating booking: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating booking: {str(e)}",
        )
        

@router.get("/ownerBookings/{owner_username}", response_model=dict, status_code=status.HTTP_200_OK)
async def owner_bookings(
    owner_username: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Add some logging to see the flow of execution
        print(f"Fetching bookings for owner: {owner_username}")

        # Query bookings for the specified owner
        query_owner_bookings = select([booking]).where(
            booking.c.ownerusername == owner_username
        )
        owner_bookings = await db.fetch_all(query_owner_bookings)

        print(f"Owner bookings: {owner_bookings}")

        # Map the raw database results to the Pydantic model
        pydantic_bookings = [BookingResponse(**booking) for booking in owner_bookings]

        return {"bookings": pydantic_bookings}

    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPExceptions to let FastAPI handle them

    except Exception as e:
        import traceback
        print(f"Error fetching owner bookings: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching owner bookings: {str(e)}",
        )

@router.get("/playerBookings/{player_username}", response_model=dict, status_code=status.HTTP_200_OK)
async def player_bookings(
    player_username: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Add some logging to see the flow of execution
        print(f"Fetching bookings for owner: {player_username}")

        # Query bookings for the specified owner
        query_player_bookings = select([booking]).where(
            booking.c.playerusername == player_username
        )
        player_bookings = await db.fetch_all(query_player_bookings)

        print(f"Player bookings: {player_bookings}")

        # Map the raw database results to the Pydantic model
        player_pydantic_bookings = [BookingResponse(**booking) for booking in player_bookings]

        return {"bookings": player_pydantic_bookings}

    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPExceptions to let FastAPI handle them

    except Exception as e:
        import traceback
        print(f"Error fetching owner bookings: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching owner bookings: {str(e)}",
        )


@router.put("/respondToBooking", response_model=dict)
async def respond_to_booking(
    response_data: RespondBookingResponse,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database),
):
    try:
        # Check if the booking exists
        query_booking = select([booking]).where(booking.c.bookingid == response_data.booking_id)
        existing_booking = await db.fetch_one(query_booking)

        if not existing_booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )

        # Check if the owner is responding to their own booking
        if existing_booking["ownerusername"] != response_data.ownerusername:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to respond to this booking",
            )

        # Update the status based on the owner's response
        new_status = "accepted" if response_data.response == "accept" else "rejected"
        query_update_status = (
            update(booking)
            .where(booking.c.bookingid == response_data.booking_id)
            .values(status=new_status)
        )
        await db.execute(query_update_status)

        return {"message": f"Booking {response_data.booking_id} {new_status.capitalize()} successfully"}

    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPExceptions to let FastAPI handle them

    except Exception as e:
        import traceback
        print(f"Error responding to booking: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error responding to booking: {str(e)}",
        )