#!/usr/bin/python3
"""New engine DBStorage"""
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os import getenv


class DBStorage:
    __engine = None
    __session = None


def __init__(self):
    """ init method """
    self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
        os.getenv('HBNB_MYSQL_USER'),
        os.getenv('HBNB_MYSQL_PWD'),
        os.getenv('HBNB_MYSQL_HOST'),
        os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)


if os.getenv('HBNB_ENV') == 'test':
    Base.metadata.drop_all(self.__engine)


def all(self, cls=None):
    """ all method """
    if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}


def new(self, obj):
    """ new method """
    self.__session.add(obj)


def save(self):
    """ save method """
    self.__session.commit()


def delete(self, obj=None):
    """ delete method """
    if obj:
        self.__session.delete(obj)
        self.save()


def reload(self):
    """ reload method """
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
    Session = scoped_session(session_factory)
    self.__session = Session()


def close(self):
    """ close method """
    if self.__session:
        self.__session.close()
