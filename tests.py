from db import *

# Test the function with parameters
if __name__ == "__main__":
    neighborhood = 'Kips Bay'
    price = 2500
    bedrooms = 2.0
    bathrooms = 1.5
    include_no_fee = False

    results = get_matching_users(
        neighborhood,
        price,
        bedrooms,
        bathrooms,
        include_no_fee
    )

    print(results)

    # Test upsert_listings with example data
    # example_listing = {
    #     "listing_id": "12345",
    #     "address": "123 Main St",
    #     "link": "http://example.com",
    #     "price": 2500.00,
    #     "neighborhood": "Example Neighborhood",
    #     "property_type": "Rental Unit",
    #     "bedrooms": 2,
    #     "bathrooms": 1.5,
    #     "first_image_link": "http://example.com/image.jpg",
    #     "no_fee": True,
    #     "listing_agency": "Example Agency",
    #     "geographical_coordinates": "40.7128,-74.0060",
    #     "timestamp": datetime.now(timezone.utc)
    # }
    #
    # added, existing = upsert_listings([example_listing])
    # print(f"Added listings: {added}")
    # print(f"Existing listings: {existing}")
