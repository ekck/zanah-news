from flask import Blueprint
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from app.models import Category, Source, Article

bp = Blueprint('admin', __name__)

# Create custom base classes for security (optional)
class SecureModelView(ModelView):
    def is_accessible(self):
        # Add authentication logic here if needed
        return True

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Add authentication logic here if needed
        return True

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

# Initialize admin with custom index view
admin = Admin(
    name='News Scraper Admin', 
    template_mode='bootstrap4',
    index_view=CustomAdminIndexView(),
    base_template='admin/master.html'
)

def init_admin(app, db):
    # Initialize the Flask-Admin extension
    admin.init_app(app)
    
    # Import views
    from .views import CategoryView, SourceView, ArticleView
    
    # Add views with categories for better organization
    admin.add_view(CategoryView(
        Category, 
        db.session, 
        name='Categories',
        category='Content Management'
    ))
    
    admin.add_view(SourceView(
        Source, 
        db.session, 
        name='Sources',
        category='Content Management'
    ))
    
    admin.add_view(ArticleView(
        Article, 
        db.session, 
        name='Articles',
        category='Content Management'
    ))

    # Add any additional configuration
    @app.context_processor
    def inject_admin_data():
        return dict(
            admin_base_template='admin/master.html',
            admin_view=admin.index_view,
            h=admin.template_helper
        )


from . import routes