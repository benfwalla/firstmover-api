import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

# Define the connection string
connection_string = URL.create(
    'postgresql',
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE')
)

# Create the engine and session
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
