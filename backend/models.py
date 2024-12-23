from config import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    spotify_token = db.Column(db.JSON)

    def __repr__(self):
        return f"<User {self.spotify_id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "spotify_id": self.spotify_id,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login
        }