from time import sleep
from threading import Thread
from autoscrape import base_scraper

class TestScraper2(Thread, base_scraper.Scraper):

	def __init__(self, session_id):
		Thread.__init__(self)
		base_scraper.Scraper.__init__(self, session_id)

	@staticmethod
	def description():
		return "Just another test scraper..."

	def run(self):
		#Scraping sequence goes here
		self.get("https://news.ycombinator.com/")
		self.destroy()



