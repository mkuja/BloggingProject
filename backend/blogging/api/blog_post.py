from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from ..auxialiry.user import author_required
from ..marshalling.schemas import BlogPostSchema
from ..auxialiry.blog_post import (
    create_new_blog_post, get_blog_post_by_id, patch_blog_post_by_id,
    delete_blog_post_by_id, get_blog_posts_by_dates
)


blp = Blueprint("Blog Post", "Blog Post",
                url_prefix="/api/v1/blog/post",
                description="CRUD blog posts.")


@blp.route("/")
class CreatePost(MethodView):
    """CRUD Blog Posts."""

    @jwt_required()
    @author_required
    @blp.arguments(BlogPostSchema)
    @blp.response(201, schema=BlogPostSchema)
    def post(self, new_post):
        """Create a new blog post."""

        if saved_post := create_new_blog_post(new_post):
            return saved_post, 201
        else:
            return {"message": "Unprocessable entity."}, 422


@blp.route("/<int:id_>")
class PostById(MethodView):
    """Methods for manipulating posts by ID."""

    @jwt_required(optional=True)
    @blp.response(200, schema=BlogPostSchema)
    def get(self, id_):
        """Get blog post by id."""

        return get_blog_post_by_id(id_)

    @jwt_required()
    @author_required
    @blp.arguments(BlogPostSchema)
    @blp.response(200, schema=BlogPostSchema)
    def patch(self, data, id_):
        """Update blog post by id.

        Only given JSON-fields will be updated."""

        result = patch_blog_post_by_id(id_, data)
        if result:
            return result, 200
        else:
            return {"message": "Unprocessable entity."}, 422

    @jwt_required()
    @author_required
    @blp.response(200)
    def delete(self, id_):
        """Delete a blog post by id.

        Returns 409 if blog post doesn't exist."""

        delete_blog_post_by_id(id_)
        return {"message": "Deleted."}, 200


@jwt_required(optional=True)
@blp.route("/by-dates/<date:from_>/<date:to>/")
class PostsByDates(MethodView):
    """Get blog posts by giving a date range."""

    @blp.response(200, schema=BlogPostSchema(many=True))
    def get(self, from_, to):
        """Get blog posts by date range.

        Both ends of the range are inclusive. Value of `any`
        to either `from_` or `to` should make the range
        extend from that end to future or long in the past."""
        return get_blog_posts_by_dates(from_, to), 200
