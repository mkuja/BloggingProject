from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    registration_date = fields.DateTime()
    is_active = fields.Bool()  # TODO: Should UI notify user if they've been banned from writing?


class BlogPostComment(Schema):
    id = fields.Int(required=False)
    nickname = fields.Str(required=False)
    blog_post = fields.Nested(BlogPost(), required=True)
    user_id = fields.Int(required=True)


class BlogPostImage(Schema):
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
