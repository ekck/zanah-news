from app import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.title