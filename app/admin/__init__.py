from flask import Blueprint
from flask_admin import Admin
from app.models import Category, Source, Article

bp = Blueprint('admin_views', __name__)
admin = Admin(name='News Scraper Admin', template_mode='bootstrap4')

def init_admin(app, db):
    admin.init_app(app)
    
    from .views import CategoryView, SourceView, ArticleView
    
    admin.add_view(CategoryView(Category, db.session, name='Categories'))
    admin.add_view(SourceView(Source, db.session, name='Sources'))
    admin.add_view(ArticleView(Article, db.session, name='Articles'))
    
    app.register_blueprint(bp)

from . import routes