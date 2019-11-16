from flask import request
from secrets import token_hex
from time import sleep
from selenium import webdriver
from autoscrape import sessions

class Scraper():

    def __init__(self, session_id):
        agent_os = request.user_agent.platform
        if agent_os == 'windows':
            self.driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
        else:
            self.driver = webdriver.Chrome('./autoscrape/chromedriver')
        #max wait for pages to load
        self.driver.set_page_load_timeout(30)
        #max wait for page elements to load
        self.driver.implicitly_wait(30)
        self.session_id = session_id
        self.sessions = sessions

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

    def get_url(self, url):
        try:
            print("get_url", url)
            self.driver.get(url)
        except Exception as e:
            print(e)

    def find_elements_by_class_name(self, query):
        try:
            self.log("find_elements_by_class_name",query)
            self.driver.find_elements_by_class_name(url)
        except Exception as e:
            self.log(e)

    def destroy(self):
        self.driver.quit()
        self.sessions.pop(self.session_id)
