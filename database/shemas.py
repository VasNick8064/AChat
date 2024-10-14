# from sqlalchemy import Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True)
#     password = Column(String)
#
# class User_messages(Base):
#     __tablename__ = 'user_messages'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     content = Column(Text)