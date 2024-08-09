import pytest
from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from . import create_app  
from book_management.models import db, Books, Users, Reviews
from book_management.schemas import BookSchema, UserSchema, ReviewSchema


class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/BookManagementSystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

class TestBase(TestCase):
    def create_app(self):
        app = create_app(TestConfig)  
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserEndpoints(TestBase):
    def test_register_user(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "User Registered Successfully")

class TestBookEndpoints(TestBase):
    def test_add_book(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='  # Base64 encoded "testuser:password123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data['title'], 'Test Book')
        self.assertEqual(data['author'], 'Test Author')

    def test_list_books(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        response = self.client.get('/books', headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        books = response.json
        self.assertGreater(len(books), 0)

    def test_get_book(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        response = self.client.get(f'/books/{book_id}', headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['title'], 'Test Book')

    def test_update_book(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        response = self.client.put(f'/books/{book_id}', json={
            'title': 'Updated Book',
            'author': 'Updated Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        updated_book = Books.query.get(book_id)
        self.assertEqual(updated_book.title, 'Updated Book')

    def test_delete_book(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        response = self.client.delete(f'/books/{book_id}', headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        deleted_book = Books.query.get(book_id)
        self.assertIsNone(deleted_book)

    def test_add_book_review(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        response = self.client.post(f'/books/{book_id}/reviews', json={
            'review': 'Great book!',
            'rating': 5
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 201)
        review = response.json
        self.assertEqual(review['review'], 'Great book!')

    def test_get_book_reviews(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        self.client.post(f'/books/{book_id}/reviews', json={
            'review': 'Great book!',
            'rating': 5
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        response = self.client.get(f'/books/{book_id}/reviews', headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        reviews = response.json
        self.assertGreater(len(reviews), 0)

    def test_get_book_summary(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'password123'})
        book_response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author'
        }, headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        book_id = book_response.json['id']
        response = self.client.get(f'/books/{book_id}/summary', headers={
            'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='
        })
        self.assertEqual(response.status_code, 200)
        summary = response.json
        self.assertEqual(summary['title'], 'Test Book')

if __name__ == '__main__':
    pytest.main()
