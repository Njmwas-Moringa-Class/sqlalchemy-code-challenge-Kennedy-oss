import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
db_directory = os.path.join(os.getcwd(), 'db')
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)
    reviews = relationship("Review", back_populates="restaurant")

    def __repr__(self):
        return f'Restaurant: {self.name}'

    def customers(self):
        unique_customers = set()
        for review in self.reviews:
            unique_customers.add(review.customer)
        return list(unique_customers)

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    reviews = relationship("Review", back_populates="customer")

    def __repr__(self):
        return f'Customer: {self.first_name} {self.last_name}'

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite_restaurant(self):
        if not self.reviews:
            return None
        highest_rating = max(review.star_rating for review in self.reviews)
        favorite_reviews = [review for review in self.reviews if review.star_rating == highest_rating]
        return favorite_reviews[0].restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def __repr__(self):
        return f'Review by {self.customer.full_name()} for {self.restaurant.name}: {self.star_rating} stars'

    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars.'

Base.metadata.create_all(engine)

