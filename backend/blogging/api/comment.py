from flask.views import MethodView
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
        if saved_comment := create_new_blog_post_comment(comment):
            return saved_comment, 201
        else:
            return {"message": "IntegrityError: Make sure parent_id or blog_post_id is correctly set."
                   }, 422


@blp.route("/<int:id_>")
class CommentById(MethodView):
    """Operations on comments by ID"""

    @blp.response(200, BlogPostComment)
    @blp.response(404)
    def get(self, id_):
        """Get comment by ID
        """
        ret = get_comment_by_id(id_)
        return ret, 200 if ret else 404

    @blp.response(200, BlogPostComment)
    @blp.response(404)
    @blp.arguments(BlogPostComment)
    def patch(self, data, id_):
        """Update a comment with new values."""

        ret = patch_comment_by_id(id_, data)
        return ret, 200 if ret else 404

