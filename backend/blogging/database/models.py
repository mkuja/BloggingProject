import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey

from sqlalchemy.orm import declarative_base, relationship

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
    registration_date = Column(DateTime, nullable=False, default=datetime.datetime.now())

    comments = relationship("Comment", back_populates="user")
    blog_posts = relationship("BlogPost", back_populates="user")



class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(20), nullable=True)
    comment = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="comments")

    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    children = relationship("Comment")


class BlogPost(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, default=datetime.datetime.now())
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)

    images = relationship("Image", back_populates="blog_post")

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





