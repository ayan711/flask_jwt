# from  flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
# from  flask_marshmallow.Marshmallow import Schema, fields, ValidationError, pre_load
from src.models import db
# from .src import app


# Custom validator
def must_not_be_ayan(data):
    print(data.isnumeric())
    if data.isnumeric():
        raise ValidationError("Can't accept this author")

class UserSchema(Schema):

    name = fields.Str(required=True)
    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BookSchema(Schema):

    Author = fields.Str(required=True,validate=must_not_be_ayan)
    name = fields.Str(required=True)
    Publisher = fields.Str(required=True)
    book_prize = fields.Int(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)