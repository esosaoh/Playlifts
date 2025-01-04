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
    
    @staticmethod
    def create_user(spotify_id, email, access_token):
        user = User.query.filter_by(spotify_id=spotify_id).first()
        if user:
            print(f"✅ User {email} already exists.")
            # Optionally update the last login time or token
            user.last_login = datetime.utcnow()
            if access_token:
                user.spotify_token = access_token
            db.session.commit()
        else:
            user = User(
                spotify_id=spotify_id,
                email=email,
                last_login=datetime.utcnow(),
                spotify_token=access_token
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ New user {email} created successfully.")
        return user