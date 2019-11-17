from copy import copy
# from secrets import token_hex
from flask import render_template, url_for, flash, redirect
from autoscrape import app, sessions, max_sessions, helpers, db
'''
from autoscrape.scraper import Scraper
'''
from autoscrape.scrapers import testscraper2
from autoscrape.models import TestDBClass, Session, LogEntry

scrapers = {
	"TestScraper2": testscraper2.TestScraper2
}

@app.route("/")
def home():
	return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html', sessions=sessions, max_sessions=max_sessions, number_of_sessions=len(sessions))

'''
@app.route("/test_scrape")
def test_scrape():
	session_id = token_hex(8)
	scraper_session = Scraper(session_id)
	scrape_url = "https://news.ycombinator.com/"
	scrape_query1 = "athing"
	scraper_output = scraper_session.test_scrape(scrape_url, scrape_query1)
	for element in scraper_output:
		db.session.add(TestDBClass(result=element, scrape_url=scrape_url, scrape_query1=scrape_query1))
	db.session.commit()
	page_output = []
	for index in db.session.query(TestDBClass):
		page_output.append(index)
	scraper_session.destroy()
	return render_template('test_scrape.html', page_output=page_output)
'''

@app.route("/create_session/<string:scraper_name>")
def create_session(scraper_name):
	Scraper = scrapers.get(scraper_name)
	if Scraper:
		if len(sessions) < max_sessions:
			#Register the session in DB
			session = Session(description=Scraper.description())
			db.session.add(session)
			db.session.commit()		
			# session_id = token_hex(8)
			#Create the session thread and store in process memory
			#first create a dummy entry to avoid multiple concurrent startups exceeding max session limit
			sessions[session.id] = "..."
			sessions[session.id] = Scraper(session.id)
			sessions[session.id].start()
			flash(f"Scraper session {session.id} has started.","success")
		else:
			flash(f"Cannot create new session - All {max_sessions} scrapers are currently busy.", "danger")
	else:
		flash(f"Cannot create session of {scraper_name} - that scraper does not exist!", "danger")
	return redirect(url_for("dashboard"))

@app.route("/view_sessions")
def view_sessions():
	return(str(sessions))

@app.route("/destroy_session/<string:session_id>")
def destroy_session(session_id):
	try:
		sessions[int(session_id)].destroy()
		flash(f"Scraper session {session_id} has been destroyed.","success")
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