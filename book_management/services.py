from flask import  request, jsonify,Response
from book_management.database import db
from book_management.models import Books,Reviews,Users
from book_management.schemas import *

def commit_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise e
        
def register_user(data):
    user = Users(**data)
    try:
        commit_data(user)
    except Exception as e:
        raise e

def add_book(data):
    new_book = Books(**data)
    try:
        commit_data(new_book)
    except Exception as e:
        raise e
    return new_book

def get_book_reviews(id):
    try:
        # Query to get reviews for the specified book
        reviews = Reviews.query.filter_by(book_id=id).all()  # Execute the query
        if not reviews:
            print("No reviews found for this book")
            return jsonify({'message': 'No reviews found for this book'})

        # Return the list of reviews
        return reviews

    except Exception as e:
        # Log the exception (for production use proper logging)
        print(f"An error occurred: {str(e)}")

        # Return a generic error message
        return jsonify({'message': 'An internal error occurred'})
    

def add_book_review(data,id):
    if not data:
        return jsonify({'message': 'No input data provided'})

    # Find the book by ID
    book = Books.query.filter_by(id=id).first()
    if not book:
        return jsonify({'message': 'Book not found'})
    # Create a new review
    new_review = Reviews(**data)
    print("new review",new_review)
    try:
        commit_data(new_review)
    except Exception as e:
        raise e

    # Return the newly created review
    return jsonify(data)

def delete_book_by_id(id):
    book = Books.query.filter_by(id=id).first()
    if not book:
        return jsonify({'message': 'Book not found'})

    # Delete the book
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify({'message': 'Book deleted successfully'})


def update_book_by_id(data,id):
    if not data:
        return jsonify({'message': 'No input data provided'})

    # Find the existing book
    book = Books.query.filter_by(id=id).first()
    if not book:
        return jsonify({'message': 'Book not found'})

    # Update book details
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.year_published = data.get('year_published', book.year_published)
    book.summary = data.get('summary', book.summary)

    # Commit changes
    try:
        db.session.commit()
    except Exception as e:
        raise e

    # Return the updated book
    return jsonify(BookSchema().dump(book))