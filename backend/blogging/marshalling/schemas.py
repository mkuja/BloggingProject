from marshmallow import Schema, fields


class User(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    registration_date = fields.DateTime()
    is_active = fields.Bool()  # TODO: Should UI notify user if they've been banned from writing?


class BlogPostImage(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    url = fields.Str()  # For sending images to client.
    data_base64 = fields.Str()  # For sending data to server.
    caption = fields.Str()


class BlogPost(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    publish_time = fields.DateTime()
    summary = fields.Str()
    content = fields.Str(required=True)
    images = fields.List(
        fields.Nested(BlogPostImage())
    )
    replies = fields.List(
        fields.Nested(lambda: BlogPost(exclude=("replies",)))
    )


class BlogPostComment(Schema):
    id = fields.Int(dump_only=True)
    nickname = fields.Str(required=False)
    blog_post = fields.Nested(BlogPost, required=True)
    user_id = fields.Int(required=True)

