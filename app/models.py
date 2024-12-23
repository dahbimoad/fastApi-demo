#this is : models.py
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone= True) , nullable=False, server_default=text('CURRENT_TIMESTAMP') )


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    published = Column(Boolean,
                       nullable=False,
                       server_default=text("FALSE"))
    created_at = Column(TIMESTAMP(timezone= True) , nullable=False, server_default=text('CURRENT_TIMESTAMP') )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('User', backref='posts')


