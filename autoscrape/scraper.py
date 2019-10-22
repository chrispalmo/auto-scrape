from flask import request
from selenium import webdriver
import time
import datetime
from autoscrape import sessions

class Scraper():

    def __init__(self, session_id = 0, sessions = sessions):
        agent_os = request.user_agent.platform
        if agent_os == 'windows':
            self.driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
        else:
            self.driver = webdriver.Chrome('./autoscrape/chromedriver')

        self.session_id = session_id
        self.sessions = sessions

    def test_scrape(self):
        print("scraping https://news.ycombinator.com/")
        self.driver.get("https://news.ycombinator.com/")
        time.sleep(1)
        try:
            print("scraping...")
            posts = self.driver.find_elements_by_class_name("athing")
            return [post.text for post in posts]

        except Exception as e:
            return e

    def quit(self):
        self.driver.quit()

    def destroy(self):
        self.driver.quit()
        self.sessions.pop(self.session_id)
