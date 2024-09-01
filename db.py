import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, Table, Column, String, Float, Boolean, Text, MetaData, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

load_dotenv()

# Define the connection string
connection_string = URL.create(
    'postgresql',
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE')
)

# Create the engine
engine = create_engine(connection_string)

# Create a metadata object
metadata = MetaData()

# Define the listings table with listing_id as the primary key
listings = Table(
    'listings', metadata,
    Column('listing_id', String, primary_key=True),
    Column('address', Text, nullable=False),
    Column('link', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('neighborhood', String, nullable=False),
    Column('property_type', String, nullable=False),
    Column('bedrooms', Float, nullable=True),
    Column('bathrooms', Float, nullable=True),
    Column('first_image_link', Text),
    Column('no_fee', Boolean, nullable=False),
    Column('listing_agency', String),
    Column('geographical_coordinates', Text),
    Column('timestamp', TIMESTAMP(timezone=True), nullable=False)
)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create the table in the database
metadata.create_all(engine)


def upsert_listings(listing_data):
    session = Session()
    added_listings = []
    existing_listings = []

    try:
        for listing in listing_data:
            # Prepare the upsert statement with do nothing on conflict
            stmt = insert(listings).values(
                listing_id=listing['listing_id'],
                address=listing['address'],
                link=listing['link'],
                price=listing['price'],
                neighborhood=listing['neighborhood'],
                property_type=listing['property_type'],
                bedrooms=listing['bedrooms'],
                bathrooms=listing['bathrooms'],
                first_image_link=listing['first_image_link'],
                no_fee=listing['no_fee'],
                listing_agency=listing['listing_agency'],
                geographical_coordinates=listing['geographical_coordinates'],
                timestamp=listing['timestamp']
            ).on_conflict_do_nothing(index_elements=['listing_id'])

            result = session.execute(stmt)
            if result.rowcount == 1:
                added_listings.append(listing['listing_id'])
            else:
                existing_listings.append(listing['listing_id'])

        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

    return added_listings, existing_listings


# Example usage
if __name__ == "__main__":
    example_listing = {
        "listing_id": "12345",
        "address": "123 Main St",
        "link": "http://example.com",
        "price": 2500.00,
        "neighborhood": "Example Neighborhood",
        "property_type": "Rental Unit",
        "bedrooms": 2,
        "bathrooms": 1.5,
        "first_image_link": "http://example.com/image.jpg",
        "no_fee": True,
        "listing_agency": "Example Agency",
        "geographical_coordinates": "40.7128,-74.0060",
        "timestamp": datetime.now(timezone.utc)  # Use timezone-aware datetime object
    }

    added, existing = upsert_listings([example_listing])
    print(f"Added listings: {added}")
    print(f"Existing listings: {existing}")
