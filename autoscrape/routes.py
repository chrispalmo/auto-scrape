from copy import copy
from flask import render_template, url_for, flash, redirect
from autoscrape import app, sessions, max_sessions, helpers, db
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

@app.route("/log/<int:session_id>")
def log(session_id):
	log_entries = LogEntry.query.filter_by(session_id=session_id).order_by(LogEntry.date.desc())
	return render_template('log.html', session_id=session_id, log_entries=log_entries)

@app.route("/create_session/<string:scraper_name>")
def create_session(scraper_name):
	Scraper = scrapers.get(scraper_name)
	if Scraper:
		if len(sessions) < max_sessions:
			#Register the session in DB
			session = Session(scraper=Scraper.__name__,description=Scraper.description())
			db.session.add(session)
			db.session.commit()		
			#Create the session thread and store in process memory
			#first create dummy entry to avoid multiple concurrent startups exceeding max session limit
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