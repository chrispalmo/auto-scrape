from flask import render_template, url_for, flash
from autoscrape import app, scraper


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/test_scrape")
def test_scrape():
		scraper_session = scraper.Scraper()
		scraper_output = scraper_session.test_scrape()
		scraper_session.quit()
		return render_template('test_scrape.html', scraper_output=scraper_output)
