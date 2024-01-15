from databases import Database
from decouple import config

# Read database configurations from environment variables or a .env file
DATABASE_URL = config('DATABASE_URL')

# Create a database instance
database = Database(DATABASE_URL)

# Dependency function to get the database
async def get_database():
    try:
        # Connect to the database
        await database.connect()
        yield database
    finally:
        # Disconnect from the database after the request is processed
        await database.disconnect()
