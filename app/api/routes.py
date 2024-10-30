from flask import jsonify
from . import bp
from app.models import Category, Article, Source
from app.scraper.scraper import NewsScraper

@bp.route('/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@ bp.route('/sources')
def get_sources():
    sources = Source.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'url': s.url} for s in sources])

@bp.route('/articles')
def get_articles():
    articles = Article.query.all()
    return jsonify([{'id': a.id, 'title': a.title, 'url': a.url, 'source': a.source.name} for a in articles])

@bp.route('/scrape')
def scrape_all_sources():
    scraper = NewsScraper()
    scraper.scrape_all_sources()
    scraper.close()
    return jsonify({'success': True})