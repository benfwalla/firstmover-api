from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, ForeignKey, TIMESTAMP, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Listing(Base):
    __tablename__ = 'listings'
    listing_id = Column(String, primary_key=True)
    address = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    neighborhood = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    bedrooms = Column(Float, nullable=True)
    bathrooms = Column(Float, nullable=True)
    first_image_link = Column(Text, nullable=True)
    no_fee = Column(Boolean, nullable=False)
    listing_agency = Column(String, nullable=True)
    geographical_coordinates = Column(Text, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)

class User(Base):
    __tablename__ = 'users'
    phone_number = Column(String, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    fcm_token = Column(String, nullable=True)

    # Correctly set up the relationship with UserSearchPreferences
    search_preferences = relationship(
        'UserSearchPreferences',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='joined'
    )

class UserSearchPreferences(Base):
    __tablename__ = 'user_search_preferences'
    search_id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, ForeignKey('users.phone_number', ondelete='CASCADE'), nullable=False)
    neighborhoods = Column(ARRAY(String), nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    bedroom_options = Column(ARRAY(Float), nullable=False)
    bathroom_threshold = Column(Float, nullable=False)
    no_fee = Column(Boolean, nullable=False)
    broker_fees = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Back-reference to User
    user = relationship(
        'User',
        back_populates='search_preferences'
    )
