from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

class CategoryView(SecureModelView):
    column_list = ['id', 'name']
    column_searchable_list = ['name']
    column_sortable_list = ['id', 'name']
    form_columns = ['name']

class SourceView(SecureModelView):
    column_list = ['id', 'name', 'url', 'category']
    column_searchable_list = ['name', 'url']
    column_sortable_list = ['id', 'name']
    form_columns = ['name', 'url', 'category']

class ArticleView(SecureModelView):
    column_list = ['id', 'title', 'url', 'published_at', 'source']
    column_searchable_list = ['title', 'url']
    column_sortable_list = ['id', 'title', 'published_at']
    form_columns = ['title', 'url', 'content', 'published_at', 'source']