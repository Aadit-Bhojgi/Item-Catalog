"""This file creates the table of our Database that are User Table,
 Categories Table and LatestItem Table"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description_cat = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description_cat,
            'id': self.id,
        }


# NOTE: time_created as the name suggests by default
#  stores the creation of the value or row inserted.
# and time_updated similarly Updates the Time
# whenever the row is updated by the user.
class LatestItem(Base):
    __tablename__ = 'latest_item'

    title = Column(String(80), nullable=False)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    item_category = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.title,
            'description': self.description,
            'id': self.id,
            'Category': self.item_category,
        }


engine = create_engine('sqlite:///sports_database.db')

Base.metadata.create_all(engine)
