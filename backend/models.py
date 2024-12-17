from config import db
import datetime

class Migrations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_user_id = db.Column(db.String(200), nullable=False)
    track_id = db.Column(db.String(200), nullable=False)
    migrated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Migration {self.spotify_user_id} - {self.track_id}>"
    
def add_migration(spotify_user_id, track_id):
    migration = Migrations(
        spotify_user_id=spotify_user_id,
        track_id=track_id,
        migrated_at=datetime.utcnow()
    )
    db.session.add(migration)
    db.session.commit()