# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse
from book_management.models import Users, Books, Reviews
from book_management.schemas import BookSchema
from book_management.database import AsyncSessionLocal

async def commit_data(session: AsyncSession, data):
    try:
        session.add(data)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e

async def register_user(data: dict):
    async with AsyncSessionLocal() as session:
        user = Users(**data)
        try:
            await commit_data(session, user)
        except Exception as e:
            raise e

async def add_book(data: dict):
    async with AsyncSessionLocal() as session:
        new_book = Books(**data)
        try:
            await commit_data(session, new_book)
        except Exception as e:
            raise e
        return data

async def get_book_reviews(id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Reviews).filter_by(book_id=id))
            reviews = result.scalars().all()
            if not reviews:
                return {'message': 'No reviews found for this book'}
            return reviews
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {'message': 'An internal error occurred'}

async def add_book_review(data: dict, id: int):
    async with AsyncSessionLocal() as session:
        if not data:
            return {'message': 'No input data provided'}

        # Find the book by ID
        result = await session.execute(select(Books).filter_by(id=id))
        book = result.scalars().first()
        if not book:
            return {'message': 'Book not found'}
        
        # Create a new review
        new_review = Reviews(**data)
        try:
            await commit_data(session, new_review)
        except Exception as e:
            raise e

        # Return the newly created review
        return data

async def delete_book_by_id(id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Books).filter_by(id=id))
            book = result.scalars().first()
            if not book:
                return {'message': 'Book not found'}

            await session.delete(book)
            await session.commit()
            return {'message': 'Book deleted successfully'}
        except Exception as e:
            await session.rollback()
            raise e

async def update_book_by_id(data: dict, id: int):
    async with AsyncSessionLocal() as session:
        if not data:
            return {'message': 'No input data provided'}

        try:
            result = await session.execute(select(Books).filter_by(id=id))
            book = result.scalars().first()
            if not book:
                return {'message': 'Book not found'}

            # Update book details
            for key, value in data.items():
                setattr(book, key, value)

            await session.commit()
            return data
        except Exception as e:
            await session.rollback()
            raise e
