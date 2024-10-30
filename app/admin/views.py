from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from wtforms import validators

class CategoryView(ModelView):
    form_base_class = SecureForm
    column_list = ('name',)
    form_columns = ('name',)
    
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        }
    }

class SourceView(ModelView):
    form_base_class = SecureForm
    column_list = ('name', 'url', 'category')
    form_columns = ('name', 'url', 'category')
    
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

class ArticleView(ModelView):
    form_base_class = SecureForm
    column_list = ('title', 'url', 'published_date', 'source')
    form_columns = ('title', 'url', 'content', 'published_date', 'source')
    
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