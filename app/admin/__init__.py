# app/admin/__init__.py
from flask import Blueprint
from flask_admin import Admin, AdminIndexView
from flask import redirect, url_for, request
from flask_login import current_user

bp = Blueprint('admin_bp', __name__)

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

admin = Admin(
    name='News Scraper Admin', 
    template_mode='bootstrap4',
    index_view=CustomAdminIndexView(),
    base_template='admin/master.html',
    url='/admin'
)

def init_admin(app, db):
    admin.init_app(app)
    
    # Import models and views here to avoid circular imports
    from app.models.category import Category
    from app.models.source import Source
    from app.models.article import Article
    from .views import CategoryView, SourceView, ArticleView
    
    # Add views with categories
    admin.add_view(CategoryView(Category, db.session, name='Categories', 
                              category='Content Management'))
    admin.add_view(SourceView(Source, db.session, name='Sources', 
                            category='Content Management'))
    admin.add_view(ArticleView(Article, db.session, name='Articles', 
                             category='Content Management'))

from . import routes