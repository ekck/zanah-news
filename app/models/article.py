from app import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    source = db.relationship('Source', backref='articles')
    is_read = db.Column(db.Boolean, default=False)  # Add this line

    def __str__(self):
        return self.title