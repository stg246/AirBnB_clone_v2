#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
   """Represents a city for a MySQL database.
    
    Inherits from SQLAlchemy Base and links to the MySQL table cities.
    
    Attributes:
        __tablename__ (str): The name of the MySQL table to store Cities.
        name (sqlalchemy String): The name of the City.
        state_id (sqlalchemy String): The state id of the City.
    """
    state_id = Column(String(60), Foreignkey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    __tablename__ = 'cities'
    places = relationship('Place', backref='cities', cascade='delete')
