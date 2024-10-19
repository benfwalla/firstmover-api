from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from .models import Listing
from .session import get_session


def upsert_listings(listing_data):
    session = get_session()
    added_listings = []
    existing_listings = []

    try:
        for listing in listing_data:
            stmt = insert(Listing).values(**listing).on_conflict_do_nothing(
                index_elements=['listing_id']
            )
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


if __name__ == "__main__":
    # Test upsert_listings with example data
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
        "timestamp": datetime.now(timezone.utc)
    }

    added, existing = upsert_listings([example_listing])
    print(f"Added listings: {added}")
    print(f"Existing listings: {existing}")

    # Test get_matching_users with example parameters
