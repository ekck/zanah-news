from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from wtforms import validators
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category

class CategoryView(ModelView):
    column_list = ['name']
    form_columns = ['name']
    
    form_args = {
        'name': {
            'label': 'Category Name',
            'validators': [validators.DataRequired()]
        }
    }

class SourceView(ModelView):
    column_list = ['name', 'url', 'category']
    form_columns = ['name', 'url', 'article_selector', 'title_selector', 'link_selector', 'category']
    
    form_args = {
        'name': {
            'label': 'Source Name',
            'validators': [validators.DataRequired()]
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
        }
    }

    def create_form(self):
        form = super(SourceView, self).create_form()
        form.category.query = Category.query
        return form

    def edit_form(self, obj):
        form = super(SourceView, self).edit_form(obj)
        form.category.query = Category.query
        return form

class ArticleView(ModelView):
    column_list = ['title', 'url', 'created_at', 'source']
    form_columns = ['title', 'url', 'content', 'source']
    
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    form_args = {
        'title': {
            'label': 'Article Title',
            'validators': [validators.DataRequired()]
        },
        'url': {
            'label': 'Article URL',
            'validators': [validators.DataRequired(), validators.URL()]
        },
        'content': {
            'label': 'Article Content',
        }
    }

    def create_form(self):
        form = super(ArticleView, self).create_form()
        form.source.query = Source.query
        return form

    def edit_form(self, obj):
        form = super(ArticleView, self).edit_form(obj)
        form.source.query = Source.query
        return form

    # Optional: Add search functionality
    column_searchable_list = ['title', 'content']
    
    # Optional: Add filters
    column_filters = ['source.name', 'created_at']
    
    # Optional: Add export functionality
    can_export = True
    export_types = ['csv', 'xlsx']
    
    # Optional: Add column descriptions
    column_descriptions = {
        'title': 'The title of the article',
        'url': 'The URL where the article can be found',
        'content': 'The main content of the article',
        'source': 'The source website of the article'
    }
    
    # Optional: Custom list formatting
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'title': lambda v, c, m, p: m.title[:50] + '...' if len(m.title) > 50 else m.title
    }
    
    # Optional: Default sort order
    column_default_sort = ('created_at', True)  # Sort by created_at descending