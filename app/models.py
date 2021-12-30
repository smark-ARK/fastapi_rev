from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, String
from sqlalchemy import Column
from .database import Base


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    url_type = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("Users", back_populates="posts")


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("Posts", back_populates="user")
