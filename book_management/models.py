from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

# Create the Base class for declarative models
Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), unique=True, nullable=False)
    author = Column(String(50), nullable=False)
    genre = Column(String(50), nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(String(500), nullable=False)

    def __repr__(self):
        return f'<book {self.title}>'

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    
    # Establish backref relationship to Book
    book = relationship('Books', backref='reviews')
    review_text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<rating {self.rating}>'
