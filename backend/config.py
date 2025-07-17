from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["https://playlifts.com", "https://www.playlifts.com"], 
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{MYSQL_PASSWORD}@localhost/migrations'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

