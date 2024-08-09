from flask import Flask
from book_management import create_app
from book_management.config import Config
from flask_sqlalchemy import SQLAlchemy
from book_management.controllers import api
from flasgger import Swagger


if __name__ == "__main__":
     flask_app = create_app()
     flask_app.register_blueprint(api)
     swagger = Swagger(flask_app)
     flask_app.run(debug=True)
    