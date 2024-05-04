#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value: str) -> None:
        """
        Overrides the default behavior of the __setattr__ method to hash the password when it is set.

        Args:
            name (str): The name of the attribute to set.
            value (Any): The value to set the attribute to.

        Returns:
            None
        """
        if name == 'password':
            value = hashlib.md5(bytes(value, 'utf-8')).hexdigest()
        return super().__setattr__(name, value)
