from book_management.database import db
from sqlalchemy import ForeignKey



class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), unique = True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<book {self.title}>'
    

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True,nullable=False)

class Reviews(db.Model):
    __tablename__ = 'reviews' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)
    
    # Establish backref relationship to Book
    book = db.relationship('Books', backref=db.backref('reviews', lazy=True))
    review_text = db.Column(db.String(500),  nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<rating {self.rating}>'
    
    