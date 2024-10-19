from sqlalchemy import and_, or_
from .session import get_session
from .models import User, UserSearchPreferences


def get_matching_users(neighborhood, price, bedrooms, bathrooms, include_no_fee):
    """
    Retrieve users whose search preferences match the given listing criteria.

    Args:
        neighborhood (str): Target neighborhood to match.
        price (float): Listing price to match against user preferences.
        bedrooms (float): Number of bedrooms in the listing.
        bathrooms (float): Number of bathrooms in the listing.
        include_no_fee (bool): Whether to include no-fee listings.

    Returns:
        list: A list of tuples containing phone numbers and search IDs of matching users.
    """
    session = get_session()
    usp = UserSearchPreferences
    u = User

    query = session.query(u.phone_number, u.fcm_token, usp.search_id).join(usp, u.phone_number == usp.phone_number)

    conditions = [
        usp.neighborhoods.any(neighborhood),  # Match neighborhood
        usp.min_price <= price,  # Match minimum price
        usp.max_price >= price,  # Match maximum price
        usp.bedroom_options.any(bedrooms),  # Match bedroom options
        bathrooms >= usp.bathroom_threshold,  # Ensure bathrooms meet threshold
        or_(include_no_fee, usp.no_fee == False),  # Include fee conditions
        or_(
            usp.broker_fees == 'bring_em_on',  # Always include broker fee listings
            and_(usp.broker_fees == 'if_10_cheaper', price <= usp.max_price * 0.9)  # Discount logic
        )
    ]

    results = query.filter(*conditions).all()
    return results

