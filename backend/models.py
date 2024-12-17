from config import db
import datetime

class Migration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_user_id = db.Column(db.String(120), nullable=False, index=True)
    track_id = db.Column(db.String(120), nullable=False)
    migrated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Migration {self.spotify_user_id} - {self.track_id}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "spotifyUserId": self.spotify_user_id,
            "trackId": self.track_id,
            "migratedAt": self.migrated_at
        }
    
def add_migration(spotify_user_id, track_id):
    migration = Migration(
        spotify_user_id=spotify_user_id,
        track_id=track_id,
        migrated_at=datetime.utcnow()
    )
    db.session.add(migration)
    db.session.commit()