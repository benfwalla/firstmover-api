from datetime import datetime
from check_apartments import check_apartments, get_listing_days_on_market
from db import upsert_listings

if __name__ == "__main__":

    print(f"Searching NYC apartments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    page_num = 1
    while page_num <= 3:

        listings = check_apartments(page=page_num)

        upsert_results = upsert_listings(listings)
        added_listings, existing_listings = upsert_results

        last_listing_on_page = listings[-1]
        listing_day_of_last_listing = get_listing_days_on_market(last_listing_on_page['link'])

        print(f"Added {len(added_listings)} listings, "
              f"{len(existing_listings)} already exist, "
              f"Days on market of last listing on page {page_num}: {listing_day_of_last_listing}")

        # Go to the next page if all the listings needed to go into the db
        # AND the final listing on the page is older than 0 days
        if len(existing_listings) == 0 and listing_day_of_last_listing == 0:
            page_num += 1
        else:
            break

