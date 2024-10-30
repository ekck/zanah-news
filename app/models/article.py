from app import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)

    def __str__(self):
        return self.title