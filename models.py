# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    url = Column(String(50))


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    url = Column(String(50))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    phone = Column(String(12))

    @property
    def json(self):
        return {'id':self.id,
                'name':self.name,
                'phone':self.phone}