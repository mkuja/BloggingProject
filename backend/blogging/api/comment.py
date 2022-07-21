from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from blogging.auxialiry.comment import (
    create_new_blog_post_comment, get_comment_by_id,
    patch_comment_by_id
)
from blogging.marshalling.schemas import BlogPostComment

blp = Blueprint("Blog Post Comment", "Blog Post Comment",
                url_prefix="/api/v1/blog/post/comment",
                description="CRUD blog post comments.")


@blp.route("/")
class CreateComment(MethodView):
    """Make comments.
    """

    @jwt_required(optional=True)  # TODO: Get optional value from database.
    @blp.arguments(BlogPostComment)
    @blp.response(201, schema=BlogPostComment)
    @blp.response(422)
    def post(self, comment):
        """Create a new blog post comment.

        Providing a `nickname` is mandatory if user is anonymous.
        Registered user cannot provide a `nickname`.
        Providing `blog_post_id` is required, unless the comment is
        a reply to another comment. Then `parent_id` is required.
        """

        if not (bool(comment.get("blog_post_id") ^ bool(comment.get("parent_id")))):
            return {"message": "Argument error: Provide one and only one of blog_post_id or parent_id."}
        test = get_jwt_identity()
        print(test)
        return
        if saved_comment := create_new_blog_post_comment(comment):
            return saved_comment, 201
        else:
            return {"message": "IntegrityError: Make sure parent_id or blog_post_id is correctly set."
                   }, 422


@blp.route("/<int:id_>")
class CommentById(MethodView):
    """Operations on comments by ID"""

    @jwt_required(optional=True)
    @blp.response(200, BlogPostComment)
    @blp.response(404)
    def get(self, id_):
        """Get comment by ID
        """
        ret = get_comment_by_id(id_)
        return ret, 200 if ret else 404

    @jwt_required()
    @blp.response(200, BlogPostComment)
    @blp.response(404)
    @blp.arguments(BlogPostComment)
    def patch(self, data, id_):
        """Update a comment with new values."""

        return patch_comment_by_id(id_, data)

