import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dotenv import load_dotenv
from utils import clean_number, extract_property_type, extract_neighborhood

load_dotenv()


def get_listing_days_on_market(url):

    api_url = f"http://api.scraperapi.com?api_key={os.getenv('SCRAPER_API_KEY')}&url={url}"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    data = response.text

    soup = BeautifulSoup(data, 'html.parser')

    days_on_market = None
    vitals_info = soup.select("div.Vitals-detailsInfo")
    for vital in vitals_info:
        title = vital.select_one("h6.Vitals-title").text.strip()
        if title == "Days On Market":
            days_on_market_text = vital.select_one("div.Vitals-data").text.strip()
            if "today" in days_on_market_text.lower():
                days_on_market = "0"
                break
            elif "day" in days_on_market_text.lower():
                days_on_market = days_on_market_text.lower().replace(" days", "").replace(" day", "").strip()
                break
    return int(days_on_market) if days_on_market is not None else None


def check_apartments(page=1):

    base_url = "https://streeteasy.com"
    search_url = f"{base_url}/for-rent/nyc?page={page}&sort_by=listed_desc"
    api_url = f"http://api.scraperapi.com?api_key={os.getenv('SCRAPER_API_KEY')}&url={search_url}"

    print(f"Searching {search_url}")

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    properties = soup.select('li.searchCardList--listItem')

    refined_property_data = []

    for property in properties:
        try:
            # Attempting to extract the full listing ID and type
            listing_id_full = property.select_one("a.listingCard-globalLink")['data-label-id']
            listing_id = listing_id_full.split('-')[0]
            listing_type = listing_id_full.split('-')[1] if '-' in listing_id_full else 'organic'
        except Exception as e:
            listing_id = None
            listing_type = 'organic'

        try:
            # Attempting to extract the address
            address = property.select_one("address").text.strip()
        except Exception as e:
            address = None

        try:
            # Attempting to extract the listing link
            link = property.select_one("a.listingCard-globalLink")['href']
        except Exception as e:
            link = None

        try:
            # Attempting to extract the price
            price = clean_number(property.select_one(".price.listingCard-priceMargin").text.strip())
        except Exception as e:
            price = None

        try:
            # Attempting to extract the property type and neighborhood
            labels = property.select("p.listingCardLabel-grey")
            neighborhood_full = ""
            property_type_full = ""
            for label in labels:
                text = label.text.strip()
                if " in " in text:
                    property_type_full = text
                    neighborhood_full = text
                    break
            neighborhood = extract_neighborhood(neighborhood_full)
            property_type = extract_property_type(property_type_full)
        except Exception as e:
            neighborhood = None
            property_type = None

        try:
            # Attempt to extract bedrooms and bathrooms dynamically
            bedrooms = None
            bathrooms = None
            details = property.select(".listingDetailDefinitionsItem")
            for detail in details:
                detail_text = detail.text.strip().lower()
                if "studio" in detail_text:
                    bedrooms = 0
                elif "bed" in detail_text:
                    bedrooms_text = detail_text.split(" bed")[0].strip()
                    bedrooms = clean_number(bedrooms_text)
                if "bath" in detail_text:
                    bathrooms_text = detail_text.split(" bath")[0].strip()
                    bathrooms = clean_number(bathrooms_text)
        except Exception as e:
            bedrooms = None
            bathrooms = None

        try:
            # Attempting to extract the first image link
            first_image = property.select_one("img.SRPCarousel-image")['src']
        except Exception as e:
            first_image = None

        try:
            # Attempting to check if the listing has a no-fee badge
            no_fee = bool(property.select_one(".NoFeeBadge"))
        except Exception as e:
            no_fee = None

        try:
            # Attempting to extract the listing agency
            listing_agency_text = property.select_one(".listingCardBottom--finePrint").text.strip()
            listing_agency = listing_agency_text.split("by ", 1)[1] if "by " in listing_agency_text else listing_agency_text
        except Exception as e:
            listing_agency = None

        try:
            # Attempting to extract the geographical coordinates
            coordinates = property.select_one("a.listingCard-globalLink")['data-map-points']
        except Exception as e:
            coordinates = None

        timestamp = datetime.now(timezone.utc)

        res = {
            "listing_id": listing_id,
            "address": address,
            "link": link,
            "price": price,
            "neighborhood": neighborhood,
            "property_type": property_type,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "first_image_link": first_image,
            "no_fee": no_fee,
            "listing_agency": listing_agency,
            "geographical_coordinates": coordinates,
            "timestamp": timestamp
        }
        if listing_type == "organic":
            refined_property_data.append(res)

    return refined_property_data


if __name__ == "__main__":
    # Example usage
    print(check_apartments())
    # Example usage of get_listing_days_on_market
    # url = "https://streeteasy.com/building/1633-de-kalb-avenue-brooklyn/2b"
    # url2 = "https://streeteasy.com/building/bridgeview-dumbo/18a"
    # print(get_listing_days_on_market(url))
    # print(get_listing_days_on_market(url2))
