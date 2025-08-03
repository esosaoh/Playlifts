from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": ["https://playlifts.com", "https://www.playlifts.com"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True,
        }
    },
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
