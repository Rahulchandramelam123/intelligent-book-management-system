# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from book_management.database import AsyncSessionLocal
from book_management.schemas import *
from book_management.models import Books, Users, Reviews
from book_management.services import register_user, add_book, update_book_by_id, delete_book_by_id, add_book_review
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from sqlalchemy import func
from datetime import datetime, timedelta
import jwt



api = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def verify_password(username: str, password: str, db: AsyncSession) -> str:
    result = await db.execute(select(Users).filter_by(username=username))
    user = result.scalars().first()
    if user and password == user.password:
        return username
    return None


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


SECRET_KEY = "your-secret-key"  # Replace with a real secret key
ALGORITHM = "HS256"

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@api.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(user: UserSchema, db: AsyncSession = Depends(get_db)):
    user_details = {
        "username": user.username,
        "password" : user.password
    }
    await register_user(user_details)
    
    return {"message": "User Registered Successfully"}

@api.post("/login")
async def login(user: UserSchema, db: AsyncSession = Depends(get_db)):
    username = await verify_password(user.username, user.password, db)
    if username:
        token = create_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Routes

@api.post("/books/", response_model=BookSchema)
async def create_book_endpoint(book: BookSchema, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    book_details = { "author": book.author ,
      "genre": book.genre,
        "summary": book.summary,
          "title": book.title, 
          "year_published": book.year_published}
    return await add_book(book_details)

@api.get("/books/", response_model=List[BookSchema])
async def read_books(db: AsyncSession = Depends(get_db),token: str = Depends(oauth2_scheme)):
    books = await db.execute(select(Books))
    return books.scalars().all()

@api.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    result = await db.execute(select(Books).filter_by(id=book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@api.put("/books/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookSchema, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    book_details = { "author": book.author ,
      "genre": book.genre,
        "summary": book.summary,
          "title": book.title, 
          "year_published": book.year_published}
    return await update_book_by_id(book_details, book_id)

@api.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    await delete_book_by_id(book_id)
    return {"message": "Book deleted"}


@api.post("/books/{id}/reviews", response_model=ReviewSchema)
async def add_book(id: int, review: ReviewSchema, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print("book_id" + str(type(review))+str(review))
    review_details = {
    "book_id":review.book_id,
    "rating": review.rating, 
    "review_text": review.review_text, 
    "user_id": review.user_id
        }
    return await add_book_review(review_details,id)
   

@api.get("/books/{id}/reviews", response_model=List[ReviewSchema])
async def get_book_reviews(id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    reviews = await db.execute(select(Reviews).filter_by(id=id))
    return reviews.scalars().all()

@api.get("/books/{id}/summary", response_model=BookSummaryRatingSchema)
async def get_book_summary(id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    books = await db.execute(select(Books.summary).filter_by(id=id))
    avg_rating = await db.execute(
            select(func.avg(Reviews.rating)).where(Reviews.book_id == id)
        )
    average_rating = avg_rating.scalars().first()
    print("average_rating" + str(average_rating))
    if books:
        res = {"summary" :books.scalars().first(), "average_rating": average_rating}
        return res
    raise HTTPException(status_code=404, detail="Book not found")
