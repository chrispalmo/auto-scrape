from copy import copy
from secrets import token_hex
from flask import render_template, url_for, flash, redirect
from autoscrape import app, scraper, sessions, max_sessions, helpers, db
from autoscrape.models import TestDBClass


@app.route("/")
def home():
	return render_template('index.html')

@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html', sessions=sessions, max_sessions=max_sessions)

@app.route("/test_scrape")
def test_scrape():
	scraper_session = scraper.Scraper()
	scrape_url = "https://news.ycombinator.com/"
	scrape_query1 = "athing"
	scraper_output = scraper_session.test_scrape(scrape_url, scrape_query1)
	for element in scraper_output:
		db.session.add(TestDBClass(result=element, scrape_url=scrape_url, scrape_query1=scrape_query1))
	db.session.commit()
	page_output = []
	for index in db.session.query(TestDBClass):
		page_output.append(index)
	scraper_session.quit()
	return render_template('test_scrape.html', page_output=page_output)

@app.route("/create_session")
def create_session():
	if len(sessions) < max_sessions:
		#random string
		#session_id = helpers.random_string_of_numbers(16)
		session_id = token_hex(8)
		#first create a dummy entry to avoid multiple concurrent startups exceeding max session limit
		sessions[session_id] = "Initializing session..."
		sessions[session_id] = scraper.Scraper(session_id)
		flash(f"Scraper session {session_id} has started.","success")
		return redirect(url_for("dashboard"))
	else:
		flash(f"Cannot create new session - All {max_sessions} scrapers are currently busy.", "danger")
		return redirect(url_for("dashboard"))

@app.route("/view_sessions")
def view_sessions():
	return(str(sessions))

@app.route("/destroy_session/<string:session_id>")
def destroy_session(session_id):
	try:
		sessions[session_id].destroy()
		flash(f"Session {session_id} has been destroyed.","success")
	except Exception as e:
		flash(f"Error: Session {session_id} does not exist!","danger")
	return redirect(url_for('dashboard'))

@app.route("/destroy_all_sessions")
def destroy_all_sessions():
	try:
		#use shallow copy to break link back to sessions object
		session_ids_to_destroy=[copy(session_id) for session_id in sessions.keys()]
		for session_id in session_ids_to_destroy:
			try:
				sessions[session_id].destroy()
			except Exception as e:
				pass
		flash("All sessions have been destroyed.", "success")
	except Exception as e:
		flash(str(e), "danger")
	return redirect(url_for('dashboard'))