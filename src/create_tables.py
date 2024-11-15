import os
from database import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Use environment variables for database credentials
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

def create_tables():
    # Create schema if it doesn't exist
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables() 