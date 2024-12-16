from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{MYSQL_PASSWORD}@localhost/migrations'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

