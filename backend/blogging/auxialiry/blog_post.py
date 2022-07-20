from datetime import date
from typing import Union, Dict

from dependency_injector.wiring import Provide
from sqlalchemy import select, delete

from blogging.containers import Container
from blogging.database.models import BlogPost
from blogging.marshalling.schemas import BlogPostSchema
from blogging.services import SessionService


def create_new_blog_post(new_post,
                         ssession: SessionService = Provide[Container.session_service]
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


def get_blog_post_by_id(id_, ssession: SessionService = Provide[Container.session_service]
                        ) -> Union[Dict, None]:
    """Get blog post by id."""

    with ssession.session as session:
        stmt = (select(BlogPost)
                .where(BlogPost.id == id_))
        post = session.scalar(stmt)
        return BlogPostSchema().dump(post) if post else None


def patch_blog_post_by_id(id_, data: Dict,
                          ssession: SessionService = Provide[Container.session_service]
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
                setattr(blog_post, val)
        session.add(blog_post)
        session.commit()
        return BlogPostSchema().dump(blog_post)


def delete_blog_post_by_id(id_, sservice: SessionService = Provide[Container.session_service]
                           ) -> bool:
    """Delete a blog post by ID.

    :returns Truthy on success. False on failure.
    """

    with sservice.session as session:
        stmt = (delete(BlogPost)
                .where(BlogPost.id == id_))
        post = session.execute(stmt)
        session.commit()
        if not post:
            return False
        return True


def get_blog_posts_by_dates(from_: date, to: date, ssession: SessionService = Provide[Container.session_service]):
    """Get blog posts by from and to dates."""

    with ssession.session as session:
        stmt = (select(BlogPost))
        posts = session.scalars(stmt)
        return BlogPostSchema(many=True).dump(posts)
