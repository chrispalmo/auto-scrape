from flask import render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from autoscrape import app, scraper, sessions, max_sessions, helpers, db
from autoscrape.models import TestDBClass, TestDBClass2, TestDBClass3
from copy import copy


@app.route("/")
def home():
	return render_template('index.html')


@app.route("/test_scrape")
def test_scrape():
	scraper_session = scraper.Scraper()
	scrape_url = "https://news.ycombinator.com/"
	filter_query1 = "athing"
	scraper_output = scraper_session.test_scrape(scrape_url, filter_query1)
	for element in scraper_output:
		db.session.add(TestDBClass3(result=element, url=scrape_url, filter_query1=filter_query1))
	db.session.commit()
	page_output = []
	for index in db.session.query(TestDBClass3):
		page_output.append(index)
	scraper_session.quit()
	return render_template('test_scrape.html', page_output=page_output)


@app.route("/create_session")
def create_session():
	if len(sessions) < max_sessions:
		#random string
		session_id = helpers.random_string_of_numbers(16)
		#first create 
		sessions[session_id] = "Initializing session..."
		sessions[session_id] = scraper.Scraper(session_id)
		return f"Scraper session {session_id} has started. easy-scrape is currently running {len(sessions)} out of a maximum capacity of {max_sessions} concurrent sessions. Check back soon for results, or watch the progress log."
	else:
		return f"Sorry, all {max_sessions} of our scrapers are busy -  please try again later!"


@app.route("/view_sessions")
def view_sessions():
	return(str(sessions))


@app.route("/destroy_session/<session_id>")
def article(session_id):
	try:
		sessions[session_id].destroy()
		return f"Session {session_id} has been destroyed."
	except Exception as e:
		return "Error: session "+str(e)+" does not exist!"


@app.route("/destroy_all_sessions")
def clear_all_sessions():
	try:
		#use shallow copy to break link back to sessions object
		session_ids_to_clear=[copy(session_id) for session_id in sessions.keys()]
		for session_id in session_ids_to_clear:
			try:
				sessions[session_id].destroy()
			except Exception as e:
				pass
		return f"All sessions have been destroyed."
	except Exception as e:
		return str(e)