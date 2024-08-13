# main.py
from fastapi import FastAPI
from book_management.controllers import api  # Import the router
from book_management.config import Config
from book_management.tables import create_tables
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Call the create_tables function during application startup
    await create_tables()
# Include the router
app.include_router(api)

# You can add more configuration if needed
