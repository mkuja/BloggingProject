import datetime
from time import time

from dependency_injector.wiring import Provide
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from blogging.containers import Container

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    username = Column(String(25), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)
    is_author = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    last_logged_out = Column(Integer, default=time)
    registration_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    comments = relationship("Comment", back_populates="user")
    blog_posts = relationship("BlogPost", back_populates="user")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(20), nullable=True)
    content = Column(Text, nullable=False)

    blog_post_id = Column(Integer, ForeignKey("blog_post.id"))
    blog_post = relationship("BlogPost", back_populates="comments")

    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="comments")

    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    children = relationship("Comment", cascade="all, delete")


class BlogPost(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, default=datetime.datetime.now)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)

    comments = relationship("Comment", back_populates="blog_post", cascade="all, delete-orphan")

    images = relationship("Image", back_populates="blog_post", cascade="all, delete-orphan")

    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="blog_posts")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    absolute_path = Column(String, nullable=False)  # Without filename
    caption = Column(String, nullable=True)
    blog_post_id = Column(Integer, ForeignKey("blog_post.id"))
    blog_post = relationship("BlogPost", back_populates="images")


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    jwt_secret_key = Column(String(80), nullable=False, default=Provide[Container.app_settings])
    anonymous_can_comment = Column(Boolean, nullable=False)
    users_can_register = Column(Boolean, nullable=False)
    verify_email = Column(Boolean, nullable=False)
    show_social_media_shares = Column(Boolean, nullable=False)
    date_and_time_format = Column(String(50), nullable=False)


