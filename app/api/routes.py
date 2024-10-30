from flask import jsonify
from flask_login import login_required
from . import bp
from app.models import Category, Article, Source
from app.scraper.scraper import NewsScraper

@bp.route('/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@bp.route('/sources')
def get_sources():
    sources = Source.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'url': s.url} for s in sources])

@bp.route('/articles')
def get_articles():
    articles = Article.query.all()
    return jsonify([{
        'id': a.id, 
        'title': a.title, 
        'url': a.url, 
        'source': a.source.name
    } for a in articles])

@bp.route('/scrape', methods=['POST'])
# @login_required
def scrape_articles():
    """
    Endpoint to trigger article scraping for all sources
    """
    try:
        scraper = NewsScraper()
        scraper.scrape_all_sources()
        return jsonify({
            'status': 'success', 
            'message': 'Articles scraped successfully.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500