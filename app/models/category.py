from app import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sources = db.relationship('Source', backref='category', lazy=True)

    def __str__(self):
        return self.name