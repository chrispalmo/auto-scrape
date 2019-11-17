from time import sleep
from threading import Thread
from autoscrape import scraper

class TestScraper2(Thread, scraper.Scraper):

	def __init__(self, session_id):
		Thread.__init__(self)
		scraper.Scraper.__init__(self, session_id)
	
	@staticmethod
	def description():
		return "Test Scraper - Mach 2. Will eventually become the template for new scrape sequences."

	def run(self):
		self.get("https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python")
		self.get("https://www.google.com/search?q=define+new+variable+in+jinja&rlz=1C1CHBD_en-GBAU781AU781&oq=define+new+variable+in+jinja&aqs=chrome..69i57j69i60j69i65j69i60l3.5439j0j7&sourceid=chrome&ie=UTF-8")
		self.get("https://jinja.palletsprojects.com/en/2.10.x/templates/")
		self.get("https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python")
		self.destroy()



