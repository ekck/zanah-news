from newspaper import Article as NewspaperArticle, Config
from app.models import Source, Article
from app import db
import logging

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.config = Config()
        self.config.browser_user_agent = 'Mozilla/5.0'

    def scrape_source(self, source):
        try:
            article = NewspaperArticle(source.url, config=self.config)
            article.download()
            article.parse()
            
            # Create new article
            new_article = Article(
                title=article.title,
                url=source.url,
                content=article.text,
                source_id=source.id
            )
            
            db.session.add(new_article)
            db.session.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error scraping {source.url}: {str(e)}")
            return False

    def scrape_all_sources(self):
        sources = Source.query.all()
        results = []
        for source in sources:
            success = self.scrape_source(source)
            results.append({
                'source': source.name,
                'success': success
            })
        return results