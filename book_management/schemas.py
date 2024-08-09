from marshmallow import Schema, fields

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str(required=True)
    year_published = fields.Integer(required=True)
    summary = fields.Str(required=True)

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class ReviewSchema(Schema):
    user_id = fields.Integer(required=True)
    book_id = fields.Integer(required=True)
    review_text = fields.Str(required=True)
    rating = fields.Integer(required=True)

class BookSummarySchema(Schema):
    summary = fields.Str(required=True)
