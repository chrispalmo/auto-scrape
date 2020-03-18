from datetime import datetime
from flask import request
from inspect import currentframe
from secrets import token_hex
from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from autoscrape import db, active_sessions
from autoscrape.helpers import time_breakdown 
from autoscrape.models import Session, LogEntry, DataEntry
from sqlalchemy import exc

print(options)


class Scraper(Thread):

    def __init__(self, session_id):
        Thread.__init__(self)
        self.session_id = session_id
        self.log(f"Initializing session...")
        self.active_sessions = active_sessions
        chrome_options = options.Options()  
        chrome_options.add_argument("--headless")  
        self.driver = webdriver.Remote(
            command_executor='http://chromedriver:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

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

    def find_element_by_xpath(self, query):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"""{func_name}("{query}")""")
            return self.driver.find_element_by_xpath(query)
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
        entry = LogEntry(message=message, session_id=self.session_id)
        try:
            db.session.add(entry)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            raise
        except Exception as e:
            raise

    def save(self, data_label, url, data=None):
        data_entry = DataEntry(
            scraper=self.__repr__(), 
            url=url,
            data_label=data_label, 
            data=data, 
            session_id=self.session_id)
        func_name = currentframe().f_code.co_name
        try:
            db.session.add(data_entry)
            db.session.commit()
            self.log(f"""{func_name}("{data_label}, {url}, {data}")""")
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            self.log(f"""ERROR WHILE SAVING: {e}""")
            raise
        finally:
            db.session.close()

    def destroy(self, completed=True):
        self.driver.quit()
        session = Session.query.filter_by(id=self.session_id).first()
        session.date_stopped = datetime.utcnow()
        scrape_time = (session.date_stopped - session.date_started).total_seconds() * 1000
        scrape_time_string = time_breakdown.time_breakdown_string(scrape_time, granularity=2)
        if completed:
            session.status = "Completed"
            self.log(f"Session completed in {scrape_time_string}.")
        else:
            session.status = "Aborted"
            self.log(f"*** Session aborted after {scrape_time_string} ***")
        db.session.commit()
        self.active_sessions.pop(self.session_id)
