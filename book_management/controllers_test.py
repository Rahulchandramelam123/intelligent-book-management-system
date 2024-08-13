# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from  app import app as api
from fastapi import FastAPI
from book_management.database import AsyncSessionLocal
from book_management.models import Books, Users, Reviews
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

# Create an instance of the FastAPI app
app = FastAPI()
app.include_router(api)

client = TestClient(app)

# Fixture to provide a database session
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

# Example test for the register endpoint
def test_register_user(db_session: AsyncSession):
    response = client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 201
    assert response.json() == {"message": "User Registered Successfully"}

# Example test for the login endpoint
def test_login_user(db_session: AsyncSession):
    # First register a user
    client.post("/register", json={"username": "testuser", "password": "testpassword"})
    
    # Then login
    response = client.post("/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Example test for creating a book
def test_create_book(db_session: AsyncSession):
    token = get_access_token()
    response = client.post(
        "/books/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Book", "author": "Test Author", "genre": "Fiction", "year_published": 2024, "summary": "A test book"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

# Example test for reading books
def test_read_books(db_session: AsyncSession):
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Example test for getting book by ID
def test_read_book(db_session: AsyncSession):
    # First create a book
    token = get_access_token()
    client.post(
        "/books/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Book", "author": "Test Author", "genre": "Fiction", "year_published": 2024, "summary": "A test book"}
    )
    
    # Then get the book by ID
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

# Helper function to get an access token
def get_access_token():
    response = client.post("/login", json={"username": "testuser", "password": "testpassword"})
    return response.json()["access_token"]

# Run the tests
if __name__ == "__main__":
    import pytest
    pytest.main()
