from flask import Blueprint
from flask_restx import  Resource
from flask_accepts import accepts, responds
from book_management.schemas import *
from flask import  request, jsonify
from book_management.database import db
from book_management.models import Books,Reviews,Users
from flask_httpauth import HTTPBasicAuth
from book_management.services import *

api = Blueprint('book_management',__name__)
auth = HTTPBasicAuth()

@auth.verify_password   
def verify_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.password == password:
        return username

@api.route("/register", methods = ['POST'])
@accepts(schema=UserSchema)
def RegisterUser():
    data = request.parsed_obj
    register_user(data)
    return "User Registered Successfully"

@api.route('/books', methods=['POST'])
@accepts(schema=BookSchema)
@responds(schema = BookSchema)
@auth.login_required
def AddBook():
    data = request.parsed_obj
    return add_book(data)

@api.route('/books', methods=['GET'])
@responds(schema = BookSchema(many=True))
@auth.login_required
def ListBooks():
    books = Books.query.all()
    return books

@api.route('/books/<int:id>', methods=['GET'])
@responds(schema = BookSchema)
@auth.login_required
def getbook(id):
    book = Books.query.filter_by(id=id).first()
    if book:
        return book
    else:
        return jsonify({"error": "book not found"})

@api.route('/books/<int:id>', methods=['PUT'])
@auth.login_required
def UpdateBookById(id):
    # Get the request data
    data = request.get_json()
    return update_book_by_id(data,id)

@api.route('/books/<int:id>', methods=['DELETE'])
@auth.login_required
def DeleteBookById(id):
    # Find the book by ID
    return delete_book_by_id(id)

@api.route('/books/<int:id>/reviews', methods=['POST'])
@auth.login_required
@accepts(schema=ReviewSchema)
@responds(schema=ReviewSchema)
def AddbookReview(id):
    # Get the request data
    data = request.parsed_obj
    return add_book_review(data,id)
    
@api.route('/books/<int:id>/reviews', methods=['GET'])
@responds(schema=ReviewSchema(many=True))
@auth.login_required
def GetBookReviews(id):
    return get_book_reviews(id)
    
@api.route('/books/<int:id>/summary', methods=['GET'])
@auth.login_required
@responds(schema=BookSummarySchema)
def get_book_summary(id):
    summary = Books.query.filter_by(id=id).first()
    return summary