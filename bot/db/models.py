__all__ = [
    'User',
    'Product',
    'Tracker',
    'Base'
]


import datetime
from sqlalchemy import DATE, VARCHAR, Column, Integer, Text, ForeignKey, Table, MetaData
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_table'

    # telegram user_id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    username = Column(VARCHAR(32), unique=False, nullable=True)

    track = Column(Integer, default=3, unique=False, nullable=False)

    reg_date = Column(DATE, default=datetime.datetime.now())

    articles = relationship("Product", back_populates='user')
    trackers = relationship("Tracker", back_populates='user')


class Product(Base):
    __tablename__ = 'product'

    article = Column(Integer, unique=False, nullable=False, primary_key=True)

    user_id = Column(Integer, ForeignKey('user_table.user_id'))

    user = relationship('User', back_populates='articles')


class Tracker(Base):
    __tablename__ = 'tracker'

    track_id = Column(Integer, nullable=False, unique=True, primary_key=True)

    article = Column(Integer, unique=False, nullable=False)

    name = Column(Text, unique=False, nullable=False)

    price = Column(Integer, unique=False, nullable=False)

    user_id = Column(Integer, ForeignKey('user_table.user_id'))

    user = relationship('User', back_populates='trackers')

    data = Column(DATE)


# postgresql+asyncpg://%(USERNAME)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(DATABASE)s