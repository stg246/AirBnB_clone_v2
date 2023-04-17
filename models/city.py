#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



class City(BaseModel):
    """ The city class, contains state ID and name """
    state_id = Column(String(60), Foreignkey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    __tablename__ = 'cities'
    places = relationship('Place', backref='cities', cascade='delete')
