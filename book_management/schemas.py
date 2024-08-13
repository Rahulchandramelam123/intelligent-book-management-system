from pydantic import BaseModel
# Schemas
class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    username: str
    password: str

class ReviewSchema(BaseModel):
    book_id : int
    user_id : int
    review_text: str
    rating: int

class BookSummaryRatingSchema(BaseModel):
    summary : str
    average_rating : float
