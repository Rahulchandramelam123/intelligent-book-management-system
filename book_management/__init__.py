from flask import Flask,jsonify
from book_management.config import Config
from book_management.database import db
from flask_sqlalchemy import SQLAlchemy
import logging
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)    
    with app.app_context():
        from book_management import models
        db.create_all()    #os.getenv('DATABASE_URL', 'sqlite:///example.db')

    logging.basicConfig(level=logging.DEBUG,  # Change to INFO or WARNING in production
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.info(e)
        if isinstance(e,HTTPException):
            res_err = {"ProgrammingErrors" : "{}".format(e)}
            return jsonify(res_err)
        
        elif isinstance(e,ValidationError):
            validation_response = {}
            validation_response["schema_errors"] = {}
            validation_response["schema_errors"][e.field_name] = [e.messages[0]]
            return validation_response, 400
        else:
            res_err = {"ProgrammingErrors" : "{}".format(e)}
            return jsonify(res_err), 500

    return app
