#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base, Restaurant, Customer, Review, session
import ipdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Make sure to import your models here
from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start the debugger
    ipdb.set_trace()

    # Example test: Fetch all restaurants and print their names
    print("Fetching all restaurants...")
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        print(restaurant.name)

    # Example test: Fetch all customers and print their full names
    print("\nFetching all customers...")
    customers = session.query(Customer).all()
    for customer in customers:
        print(customer.full_name())

    # Example test: Fetch all reviews and print them
    print("\nFetching all reviews...")
    reviews = session.query(Review).all()
    for review in reviews:
        print(review.full_review())



