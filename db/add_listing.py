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

