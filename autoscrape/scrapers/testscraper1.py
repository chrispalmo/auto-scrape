from threading import Thread
from autoscrape import base_scraper


class TestScraper1(Thread, base_scraper.Scraper):

    def __init__(self, session_id):
        Thread.__init__(self)
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        return "Scrapes YCHN post titles"

    def run(self):
        # Scraping sequence goes here. Logging is taken care of by the base_scraper base class for standard browser functions.
        try:
            # Get top YCHN posts
            url = "https://news.ycombinator.com/"
            self.get(url)
            elements = self.find_elements_by_class_name('storylink')
            elements_text_list = [element.text for element in elements]
            for element in elements_text_list:
                self.save(
                    'Post Title', 
                    url,
                    element)
        except Exception as e:
            self.log(e)

        self.destroy()
        