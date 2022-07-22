import datetime
from datetime import date
from typing import Union, Dict, Literal

from dependency_injector.wiring import Provide
from sqlalchemy import select, delete

from blogging.di.db_services_container import DBServicesContainer
from blogging.database.models import BlogPost
from blogging.marshalling.schemas import BlogPostSchema
from blogging.di.session_service import SessionService


def create_new_blog_post(new_post,
                         ssession: SessionService = Provide[DBServicesContainer.session_service]
                         ) -> Union[None, Dict]:
    """Create a new blog post."""

    try:
        with ssession.session as session:
            post = BlogPost(**new_post)
            session.add(post)
            session.commit()
            return BlogPostSchema().dump(post)
    except Exception as e:
        raise e


def get_blog_post_by_id(id_, ssession: SessionService = Provide[DBServicesContainer.session_service]
                        ) -> Union[Dict, None]:
    """Get blog post by id."""

    with ssession.session as session:
        stmt = (select(BlogPost)
                .where(BlogPost.id == id_))
        post = session.scalar(stmt)
        return BlogPostSchema().dump(post) if post else None


def patch_blog_post_by_id(id_, data: Dict,
                          ssession: SessionService = Provide[DBServicesContainer.session_service]
                          ) -> Union[Dict, None]:
    """Alter given fields of a blog post with given id."""

    with ssession.session as session:
        stmt = (select(BlogPost)
                .where(BlogPost.id == id_))
        blog_post = session.scalar(stmt)
        if not blog_post:
            return
        for key, val in data.items():
            if hasattr(blog_post, key):
                setattr(blog_post, key, val)
        session.add(blog_post)
        session.commit()
        return BlogPostSchema().dump(blog_post)


def delete_blog_post_by_id(id_,
                           sservice: SessionService = Provide[DBServicesContainer.session_service]
                           ) -> bool:
    """Delete a blog post by ID.

    :returns True on success. False on failure.
    """

    with sservice.session as session:
        stmt = (delete(BlogPost)
                .where(BlogPost.id == id_))
        session.execute(stmt)
        session.commit()


def get_blog_posts_by_dates(from_: Union[date, Literal["any"]],
                            to:  Union[date, Literal["any"]],
                            reverse=False,
                            ssession: SessionService = Provide[DBServicesContainer.session_service]):
    """Get blog posts by from and to dates.
    """

    if to == "any":
        today = date.today()
        to = datetime.datetime(day=today.day, month=today.month, year=today.year + 2)
    if from_ == "any":
        from_ = datetime.datetime(day=1, month=1, year=1900)

    from_datetime = datetime.datetime(day=from_.day, month=from_.month, year=from_.year)
    to_datetime = datetime.datetime(day=to.day, month=to.month,
                                    year=to.year, hour=23,
                                    minute=59, second=59)
    if from_ == "any":
        from_datetime = datetime.datetime(day=1, month=1, year=1900)
    if to == "any":
        to_datetime = datetime.datetime(day=1, month=1, year=datetime.date.today().year+1)
    with ssession.session as session:
        stmt = (select(BlogPost)
                .where(BlogPost.published < to_datetime)
                .where(BlogPost.published > from_datetime)
                .order_by(BlogPost.published))
        posts = session.scalars(stmt)
        retval = BlogPostSchema(many=True).dump(posts)
        if reverse:
            retval.reverse()
        return retval
