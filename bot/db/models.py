import datetime
from sqlalchemy import DATE, VARCHAR, Column, Integer, Text, ForeignKey, Table, MetaData
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass


# user = Table(
#     "user",
#     Base.metadata,
#     Column("user_id", Integer, unique=True, nullable=False, primary_key=True),
#     Column("username", VARCHAR(32), unique=False, nullable=True),
#     Column("track", Integer, default=3, unique=False, nullable=False),
#     Column("regdate", DATE, default=datetime.datetime.now())
# )

# product = Table(
#     "product",
#     Base.metadata,
#     Column("article", Integer, unique=False, nullable=False),
#     Column("user_id", ForeignKey('user.user_id'))
# )


class User(Base):
    __tablename__ = 'user'

    # telegram user_id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    username = Column(VARCHAR(32), unique=False, nullable=True)

    track = Column(Integer, default=3, unique=False, nullable=False)

    reg_date = Column(DATE, default=datetime.datetime.today())

    articles = relationship("Product", back_populates='user')


class Product(Base):
    __tablename__ = 'product'

    article = Column(Integer, unique=False, nullable=False)

    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)

    user = relationship('User', back_populates='articles')

# class Tracker(BaseModel):
#     __tablename__ = 'tracker'

#     article = Column(Integer, unique=False, nullable=False)

#     name = Column(Text, unique=False, nullable=False)

#     price = Column(Integer, unique=False, nullable=False)

#     user_id = Column(ForeignKey('user.user_id'))

#     data = Column(DATE)
