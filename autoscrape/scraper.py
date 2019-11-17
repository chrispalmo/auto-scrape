from flask import request
from inspect import currentframe
from secrets import token_hex
from time import sleep
from selenium import webdriver
from autoscrape import db, sessions
from autoscrape.models import LogEntry

class Scraper():

    def __init__(self, session_id):
        self.session_id = session_id
        self.log(f"Initializing session...")
        self.sessions = sessions

        agent_os = request.user_agent.platform
        if agent_os == 'windows':
            self.driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
        else:
            self.driver = webdriver.Chrome('./autoscrape/chromedriver')

        #max wait for pages to load
        self.driver.set_page_load_timeout(30)
        #max wait for page elements to load
        self.driver.implicitly_wait(30)
        self.log(f"Session initialization complete.")

    def test_scrape(self, url, filter_query1):
        print(url)
        self.driver.get(url)
        sleep(1)
        try:
            print("scraping...")
            elements = self.driver.find_elements_by_class_name(filter_query1)
            return [element.text for element in elements]

        except Exception as e:
            return e

    def get(self, url):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"{func_name}({url})")
            self.driver.get(url)
        except Exception as e:
            print(e)

    def find_elements_by_class_name(self, query):
        try:
            func_name = currentframe().f_code.co_name
            self.log(f"{func_name}({url})")
            self.driver.find_elements_by_class_name(url)
        except Exception as e:
            self.log(e)

    def log(self, message):
        entry = LogEntry(message=message, session_id=self.session_id)
        db.session.add(entry)
        db.session.commit()

    def destroy(self):
        self.driver.quit()
        self.sessions.pop(self.session_id)
