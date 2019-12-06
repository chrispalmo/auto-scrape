from copy import copy
from datetime import datetime
from flask import render_template, url_for, flash, redirect, Response
from autoscrape import app, active_sessions, max_active_sessions, db
from autoscrape.helpers import db_query_output_to_csv 
from autoscrape.scrapers import testscraper1, testscraper2
from autoscrape.models import TestDBClass, Session, LogEntry, DataEntry

scrapers = {
	"TestScraper1": testscraper1.TestScraper1,
	"TestScraper2": testscraper2.TestScraper2
}


@app.route("/download/session_data/<int:session_id>")
def download_session_data(session_id):
	
	data_entries = DataEntry.query.filter_by(session_id=session_id).order_by(DataEntry.timestamp.asc())
	csv = db_query_output_to_csv(

		query_output=data_entries, 
		columns_to_exclude=["_sa_instance_state", "id"])
	return Response(
		csv,
		mimetype="text/csv",
		headers={"Content-disposition":
			f"attachment; filename={datetime.now().strftime('%Y%m%d_%H%M%S_')}_session_{session_id}.csv"})

@app.route("/download/session_history")
def download_session_history():
	csv = db_query_output_to_csv(
		query_output=Session.query.all(), 
		columns_to_exclude=["_sa_instance_state", "id"])
	return Response(
		csv,
		mimetype="text/csv",
		headers={"Content-disposition":
			f"attachment; filename={datetime.now().strftime('%Y%m%d_%H%M%S_')}sessions.csv"})


@app.route("/")
def home():
	return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
	active_sessions = Session.query.filter(Session.status=="Active").order_by(Session.date_started.desc())
	past_sessions = Session.query.filter(Session.status!="Active").order_by(Session.date_stopped.desc())
	return render_template('dashboard.html',
		scrapers=scrapers,
		max_active_sessions=max_active_sessions,
		active_sessions=active_sessions,
		number_of_active_sessions=active_sessions.count(),
		past_sessions=past_sessions,
		number_of_past_sessions=past_sessions.count()
	)


@app.route("/session_data/<int:session_id>")
def session_data(session_id):
	session = Session.query.get_or_404(session_id)
	data_entries = DataEntry.query.filter_by(session_id=session_id).order_by(DataEntry.timestamp.desc())
	return render_template('session_data.html',
						   session=session,
						   data_entries=data_entries,
							data_entries_length=data_entries.count()
	)


@app.route("/log/<int:session_id>")
def log(session_id):
	session = Session.query.get_or_404(session_id)
	log_entries = LogEntry.query.filter_by(session_id=session_id).order_by(LogEntry.date.desc())
	data_entries = DataEntry.query.filter_by(session_id=session_id).order_by(DataEntry.timestamp.desc())
	return render_template('log.html', 
		session=session, 
		log_entries=log_entries,
		log_entries_length=log_entries.count()
	)


@app.route("/create_session/<string:scraper_name>")
def create_session(scraper_name):
	Scraper = scrapers.get(scraper_name)
	if Scraper:
		if len(active_sessions) < max_active_sessions:
			#Register the session in DB
			session = Session(scraper=Scraper.__name__,description=Scraper.description())
			db.session.add(session)
			db.session.commit()		
			#Create the session thread and store in process memory
			#first create dummy entry to avoid multiple concurrent startups exceeding max session limit
			active_sessions[session.id] = "..."
			active_sessions[session.id] = Scraper(session.id)
			active_sessions[session.id].start()
			flash(f"Scraper session {session.id} has started.","success")
		else:
			flash(f"Cannot create new session - All {max_active_sessions} scrapers are currently busy.", "danger")
		return redirect(url_for("dashboard"))
	else:
		flash(f"Cannot create session of {scraper_name} - that scraper does not exist!", "danger")
	return redirect(url_for("log", session_id=session.id))


@app.route("/abort_session/<string:session_id>")
def abort_session(session_id):
	try:
		active_sessions[int(session_id)].destroy(completed=False)
		flash(f"Scraper session {session_id} has been Aborted.","success")
	except Exception as e:
		flash(f"Unable to abort session {session_id}. Session is no longer active or does not exist.","danger")
	return redirect(url_for('dashboard'))


@app.route("/delete_session_record/<string:session_id>")
def delete_session_record(session_id):
	try:
		Session.query.filter_by(id=session_id).delete()
		LogEntry.query.filter_by(session_id=session_id).delete()
		DataEntry.query.filter_by(session_id=session_id).delete()
		db.session.commit()
		flash(f"Session {session_id} and all scraped data  has been deleted.", "success")
	except Exception as e:
		flash(f"Error ({e}): Session {session_id} could not be deleted.", "danger")
	return redirect(url_for('dashboard'))


@app.route("/abort_all_active_sessions")
def abort_all_active_sessions():
	try:
		#use shallow copy to break link back to active_sessions object
		session_ids_to_destroy=[copy(session_id) for session_id in active_sessions.keys()]
		for session_id in session_ids_to_destroy:
			try:
				active_sessions[session_id].destroy(completed=False)
			except Exception as e:
				pass
		flash("All active sessions have been aborted.", "success")
	except Exception as e:
		flash(str(e), "danger")
	return redirect(url_for('dashboard'))