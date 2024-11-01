# app/admin/views.py
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user
from wtforms import validators
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.category import Category  # Ensure you import your models
from app.models.source import Source  # Ensure you import your models

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
    
    # Add form validation
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        }
    }

class SourceView(SecureModelView):
    column_list = ['id', 'name', 'url', 'category']
    column_searchable_list = ['name', 'url']
    column_sortable_list = ['id', 'name']
    form_columns = ['name', 'url', 'category']
    
    # Add form validation and relationship configuration
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        },
        'url': {
            'validators': [validators.DataRequired(), validators.URL()]
        },
        'category': {
            'validators': [validators.DataRequired()]
        }
    }
    
    # Configure how relationships are displayed
    column_formatters = {
        'category': lambda v, c, m, p: m.category.name if m.category else ''
    }

    # Override the scaffold_form method to use QuerySelectField
    def scaffold_form(self):
        form_class = super(SourceView, self).scaffold_form()
        form_class.category = QuerySelectField(
            'Category',
            query_factory=lambda: Category.query.order_by(Category.name),
            get_label='name',
            allow_blank=False
        )
        return form_class

class ArticleView(SecureModelView):
    column_list = ['id', 'title', 'url', 'published_at', 'source']
    column_searchable_list = ['title', 'url']
    column_sortable_list = ['id', 'title', 'published_at']
    form_columns = ['title', 'url', 'content', 'published_at', 'source']
    
    # Add form validation and relationship configuration
    form_args = {
        'title': {
            'validators': [validators.DataRequired()]
        },
        'url': {
            'validators': [validators.DataRequired(), validators.URL()]
        },
        'source': {
            'validators': [validators.DataRequired()]
        }
    }
    
    # Configure how relationships are displayed
    column_formatters = {
        'source': lambda v, c, m, p: m.source.name if m.source else ''
    }

    # Override the scaffold_form method to use QuerySelectField for source
    def scaffold_form(self):
        form_class = super(ArticleView, self).scaffold_form()
        form_class.source = QuerySelectField(
            'Source',
            query_factory=lambda: Source.query.order_by(Source.name),
            get_label='name',
            allow_blank=False
        )
        return form_class