# intelligent-book-management-system

#rest end points

POST /register : to register user
payload {
    "username": "username",
    "password":"password"
}
POST /books: Add a new book.
payload{
        "author": "author",
        "genre": "genre of book",
        "summary": "summary of book",
        "title": "title of book",
        "year_published": 1988
}
GET /books: Retrieve all books.
GET /books/<id> : Retrieve a specific book by its ID.
PUT /books/<id> : Update a book's information by its ID.
payload{
        "author": "author",
        "genre": "genre of book",
        "summary": "summary of book",
        "title": "title of book",
        "year_published": 1988
}
DELETE /books/<id>: Delete a book by its ID.
POST /books/<id>/reviews: Add a review for a book.
payload{
        "book_id": 10,
        "rating": 4,
        "review_text": "review",
        "user_id": 1
 }
GET /books/<id>/reviews: Retrieve all reviews for a book.
GET /books/<id>/summary: Get a summary and aggregated rating for
a book.


#app deployed on aws 3.25.142.198:8000
