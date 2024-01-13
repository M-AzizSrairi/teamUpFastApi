from databases import Database
from decouple import config

# Read database configurations from environment variables or a .env file
DATABASE_URL = config('DATABASE_URL')

# Create a database instance
database = Database(DATABASE_URL)
