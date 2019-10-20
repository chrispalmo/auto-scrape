from flask import render_template, url_for, flash, request
from autoscrape import app, scraper


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/test_scrape")
def test_scrape():
    agent_os = request.user_agent.platform
    scraper.test_scrape(agent_os)
    return render_template('test_scrape.html', agent_os=agent_os)
