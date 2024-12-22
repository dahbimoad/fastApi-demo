#this is : models.py
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    email = Column(String , nullable=False, unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone= True) , nullable=False, server_default=text('now()') )


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    published = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP(timezone= True) , nullable=False, server_default=text('now()') )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('User', backref='posts')


