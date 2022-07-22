from marshmallow import Schema, fields
from marshmallow.fields import DateTime

from blogging.marshalling.converters import MyDateTimeField


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    registration_date = fields.Str(required=True, dump_only=True)
    last_logged_out = fields.Int(dump_only=True)
    is_active = fields.Bool()
    message = fields.Str(dump_only=True)


class UserPatchSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    password = fields.Str(load_only=True)
    username = fields.Str()
    email = fields.Str()
    registration_date = fields.Str(dump_only=True)
    is_active = fields.Bool()
    message = fields.Str(dump_only=True)


class Auth(Schema):
    username = fields.Str(load_only=True, required=True)
    password = fields.Str(load_only=True, required=True)
    token = fields.Str(dump_only=True, required=True)
    refresh_token = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)


class BlogPostImage(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    url = fields.Str()  # For sending images to client.
    data_base64 = fields.Str()  # For sending data to server.
    caption = fields.Str()


class BlogPostComment(Schema):
    id = fields.Int(dump_only=True)
    nickname = fields.Str()
    content = fields.Str(required=True)

    blog_post_id = fields.Int()
    user_id = fields.Int()

    children = fields.Nested(lambda: BlogPostComment(many=True))

    parent_id = fields.Int()


class BlogPostSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    published = MyDateTimeField()
    summary = fields.Str()
    content = fields.Str(required=True)
    comments = fields.Nested(BlogPostComment(), many=True)
    images = fields.List(
        fields.Nested(BlogPostImage())
    )


class SettingsSchema(Schema):
    id = fields.Int(dump_only=True)
    anonymous_can_comment = fields.Boolean()
    users_can_register = fields.Boolean()
    verify_email = fields.Boolean()
    show_social_media_shares = fields.Boolean()
    use_comment_captcha_for_anonymous = fields.Boolean()
    use_comment_captcha_for_registered = fields.Boolean()
    date_and_time_format = fields.Str()
