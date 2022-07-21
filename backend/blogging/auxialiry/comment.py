from typing import Dict, Union

import psycopg2
import sqlalchemy.exc
from dependency_injector.wiring import Provide
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from blogging.containers import Container
from blogging.database.models import Comment
from blogging.marshalling.schemas import BlogPostComment
from blogging.services import SessionService


def create_new_blog_post_comment(comment,
                                 ssession: SessionService = Provide[Container.session_service]
                                 ) -> Dict:
    """Create a new blog post."""

    with ssession.session as session:
        try:
            post = Comment(**comment)
            session.add(post)
            return_value = BlogPostComment().dump(post)
            session.commit()
            return return_value
        except IntegrityError as e:
            return


def get_comment_by_id(id_,
                      ssession: SessionService = Provide[Container.session_service]
                      ) -> Union[Dict, None]:
    """Get comment by id_"""

    with ssession.session as session:
        stmt = (select(Comment)
                .where(Comment.id == id_))
        comment = session.scalar(stmt)
        if comment:
            return BlogPostComment().dump(comment)
        return


def patch_comment_by_id(id_, data: Dict,
                        ssession: SessionService = Provide[Container.session_service]
                        ) -> Union[Dict, None]:
    """Patch a comment by id."""

    data = {k: v for k, v in data.items()
            if k != "id" or k != "user_id" or k != "children"
            or k != "blog_post_id" or k != "parent_id"}
    with ssession.session as session:
        stmt = (select(Comment)
                .where(Comment.id == id_))
        comment = session.scalar(stmt)
        if not comment:
            return
        for k, v in data.items():
            if hasattr(comment, k):
                setattr(comment, k, v)
        session.add(comment)
        session.commit()
        return BlogPostComment().dump(comment)
