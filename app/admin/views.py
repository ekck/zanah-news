from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.actions import action
from wtforms import validators
from flask import flash
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category
from app import db

class BaseModelView(ModelView):
    """Base Model View with common settings"""
    can_export = True
    export_types = ['csv', 'xlsx']
    page_size = 50
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class CategoryView(BaseModelView):
    """View for managing news categories"""
    column_list = ['name', 'sources']
    form_columns = ['name']
    
    column_searchable_list = ['name']
    column_default_sort = 'name'
    
    column_formatters = {
        'sources': lambda v, c, m, p: f"{len(m.sources)} sources"
    }
    
    column_descriptions = {
        'name': 'Category name (e.g., Politics, Technology, Sports)',
        'sources': 'Number of news sources in this category'
    }
    
    form_args = {
        'name': {
            'label': 'Category Name',
            'validators': [validators.DataRequired(), validators.Length(max=100)]
        }
    }

    list_template = 'admin/category_list.html'

    def on_model_change(self, form, model, is_created):
        """Ensure category name is capitalized"""
        model.name = model.name.strip().title()

class SourceView(BaseModelView):
    """View for managing news sources"""
    column_list = ['name', 'url', 'category', 'articles']
    form_columns = ['name', 'url', 'article_selector', 'title_selector', 
                   'link_selector', 'category']
    
    column_searchable_list = ['name', 'url']
    column_filters = ['category.name']
    column_default_sort = 'name'
    
    column_formatters = {
        'articles': lambda v, c, m, p: f"{len(m.articles)} articles",
        'url': lambda v, c, m, p: f'<a href="{m.url}" target="_blank">{m.url}</a>'
    }
    
    column_descriptions = {
        'name': 'Name of the news source',
        'url': 'Homepage URL of the news source',
        'article_selector': 'CSS selector for article containers',
        'title_selector': 'CSS selector for article titles',
        'link_selector': 'CSS selector for article links',
        'category': 'Category this source belongs to'
    }

    form_args = {
        'name': {
            'label': 'Source Name',
            'validators': [validators.DataRequired(), validators.Length(max=100)]
        },
        'url': {
            'label': 'Source URL',
            'validators': [validators.DataRequired(), validators.URL()]
        },
        'article_selector': {
            'label': 'Article Selector',
            'validators': [validators.DataRequired()]
        },
        'title_selector': {
            'label': 'Title Selector',
            'validators': [validators.DataRequired()]
        },
        'link_selector': {
            'label': 'Link Selector',
            'validators': [validators.DataRequired()]
        },
        'category': {
            'label': 'Category',
            'validators': [validators.DataRequired()]
        }
    }

    def create_form(self):
        form = super(SourceView, self).create_form()
        form.category.query = Category.query.order_by(Category.name)
        return form

    def edit_form(self, obj):
        form = super(SourceView, self).edit_form(obj)
        form.category.query = Category.query.order_by(Category.name)
        return form

    def on_model_change(self, form, model, is_created):
        """Ensure URL starts with http:// or https://"""
        if not model.url.startswith(('http://', 'https://')):
            model.url = 'https://' + model.url

class ArticleView(BaseModelView):
    """View for managing articles"""
    column_list = ['title', 'url', 'created_at', 'source', 'is_read']
    form_columns = ['title', 'url', 'content', 'source', 'is_read']
    
    column_searchable_list = ['title', 'content']
    column_filters = ['source.name', 'created_at', 'source.category.name', 'is_read']
    column_default_sort = ('created_at', True)
    
    column_descriptions = {
        'title': 'The title of the article',
        'url': 'The URL where the article can be found',
        'content': 'The main content of the article',
        'source': 'The source website of the article',
        'is_read': 'Whether the article has been marked as read',
        'created_at': 'When the article was added to the database'
    }
    
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'title': lambda v, c, m, p: m.title[:50] + '...' if len(m.title) > 50 else m.title,
        'url': lambda v, c, m, p: f'<a href="{m.url}" target="_blank">View</a>',
        'is_read': lambda v, c, m, p: '✓' if m.is_read else '✗'
    }
    
    form_args = {
        'title': {
            'label': 'Article Title',
            'validators': [validators.DataRequired(), validators.Length(max=200)]
        },
        'url': {
            'label': 'Article URL',
            'validators': [validators.DataRequired(), validators.URL()]
        },
        'content': {
            'label': 'Article Content',
        },
        'is_read': {
            'label': 'Mark as Read'
        }
    }

    def create_form(self):
        form = super(ArticleView, self).create_form()
        form.source.query = Source.query.order_by(Source.name)
        return form

    def edit_form(self, obj):
        form = super(ArticleView, self).edit_form(obj)
        form.source.query = Source.query.order_by(Source.name)
        return form

    @action('mark_read', 'Mark as Read', 'Are you sure you want to mark selected articles as read?')
    def action_mark_read(self, ids):
        try:
            query = Article.query.filter(Article.id.in_(ids))
            count = query.update({"is_read": True}, synchronize_session='fetch')
            db.session.commit()
            flash(f'{count} articles were successfully marked as read.', 'success')
        except Exception as ex:
            flash(f'Failed to mark articles as read. {str(ex)}', 'error')
            db.session.rollback()

    @action('mark_unread', 'Mark as Unread', 'Are you sure you want to mark selected articles as unread?')
    def action_mark_unread(self, ids):
        try:
            query = Article.query.filter(Article.id.in_(ids))
            count = query.update({"is_read": False}, synchronize_session='fetch')
            db.session.commit()
            flash(f'{count} articles were successfully marked as unread.', 'success')
        except Exception as ex:
            flash(f'Failed to mark articles as unread. {str(ex)}', 'error')
            db.session.rollback()

    