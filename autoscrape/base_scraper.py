from datetime import datetime
from flask import request
from inspect import currentframe
from secrets import token_hex
from time import sleep
from selenium import webdriver
from autoscrape import db, active_sessions
from autoscrape.models import Session, LogEntry, DataEntry
from sqlalchemy import exc

class Scraper():

    def __init__(self, session_id):
        self.session_id = session_id
        self.log(f"Initializing session...")
        self.active_sessions = active_sessions

        agent_os = request.user_agent.platform
        if agent_os == 'windows':
            self.driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
        else:
            self.driver = webdriver.Chrome('./autoscrape/chromedriver')

        #max wait for pages to load
        self.driver.set_page_load_timeout(30)
        #max wait for page elements to load
        self.driver.implicitly_wait(30)
        self.log(f"Initialization complete.")

    def get(self, url):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"""{func_name}("{url}")""")
            self.driver.get(url)
        except Exception as e:
            self.log(e)

    def find_elements_by_xpath(self, query):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"""{func_name}("{query}")""")
            return self.driver.find_elements_by_xpath(query)
        except Exception as e:
            self.log(e)        

    def find_elements_by_class_name(self, query):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"""{func_name}("{query}")""")
            return self.driver.find_elements_by_class_name(query)
        except Exception as e:
            self.log(e)

    def log(self, message):
        try:
            entry = LogEntry(message=message, session_id=self.session_id)
            db.session.add(entry)
            db.session.commit()
        except:
            pass

    def save(self, query, element_1, element_2, element_3, element_4, element_5):
        data_entry = DataEntry(query=query, element_1=element_1,
                               element_2=element_2, element_3=element_3,
                               element_4=element_4, element_5=element_5)
        func_name = currentframe().f_code.co_name
        try:
            db.session.add(data_entry)
            db.session.commit()
            self.log(f"""{func_name}("{query}")""")
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            self.log(f"""{func_name}("{e}")""")
        finally:
            db.session.close()


    def destroy(self, completed=True):
        self.driver.quit()
        session = Session.query.filter_by(id=self.session_id).first()
        if completed:
            session.status = "Completed"
            self.log("Session completed.")
        else:
            session.status = "Aborted"
            self.log("*** Session aborted ***")
        session.date_stopped = datetime.utcnow()
        db.session.commit()
        self.active_sessions.pop(self.session_id)
