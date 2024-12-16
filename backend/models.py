from config import db
import datetime

class Migrations(db.model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_user_id = db.Column(db.String(200), nullable=False)
    track_id = db.Column(db.String(200), nullable=False)
    migrated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Migration {self.spotify_user_id} - {self.track_id}>"