from app import db

class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    article_selector = db.Column(db.String(200), nullable=False)
    title_selector = db.Column(db.String(200), nullable=False)
    link_selector = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    articles = db.relationship('Article', backref='source', lazy=True)

    def __str__(self):
        return self.name