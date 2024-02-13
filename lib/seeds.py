from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review

# Create an engine that connects to the SQLite database
engine = create_engine('sqlite:///db/restaurants.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create sample restaurants
restaurant1 = Restaurant(name="The Pizza Place", price=2)
restaurant2 = Restaurant(name="Fine Dining & Co", price=4)

# Create sample customers
customer1 = Customer(first_name="John", last_name="Doe")
customer2 = Customer(first_name="Jane", last_name="Doe")

# Create sample reviews
review1 = Review(star_rating=5, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=3, restaurant=restaurant1, customer=customer2)
review3 = Review(star_rating=4, restaurant=restaurant2, customer=customer1)

# Add and commit the records to the database
session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2, review3])
session.commit()

print("Database seeded!")


