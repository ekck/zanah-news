from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from app.models import Source, Article
from app import db

class NewsScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_source(self, source):
        try:
            self.driver.get(source.url)
            articles = self.driver.find_elements(By.CSS_SELECTOR, source.article_selector)
            
            for article in articles:
                try:
                    title = article.find_element(By.CSS_SELECTOR, source.title_selector).text
                    url = article.find_element(By.CSS_SELECTOR, source.link_selector).get_attribute('href')
                    
                    # Check if article already exists
                    if not Article.query.filter_by(url=url).first():
                        new_article = Article(
                            title=title,
                            url=url,
                            source_id=source.id
                        )
                        db.session.add(new_article)
                except Exception as e:
                    print(f"Error scraping article: {str(e)}")
                    continue
            
            db.session.commit()
            
        except Exception as e:
            print(f"Error scraping source {source.name}: {str(e)}")
            
    def scrape_all_sources(self):
        sources = Source.query.all()
        for source in sources:
            self.scrape_source(source)
            
    def close(self):
        self.driver.quit()