from flask.views import MethodView
from flask_smorest import Blueprint

from ..marshalling.schemas import BlogPost


blp = Blueprint(BlogPost, "Blog Post",
                url_prefix="/api/v1/blog/post",
                description="CRUD blog posts.")


