from autoscrape import base_scraper

# Replace "ScraperName" to give your scraper a unique name. 
class ScraperName(base_scraper.Scraper):
    """
    Scrapers must inherit the base_scraper.Scraper class.
    This allows familiar Selenium functions such as "get", 
    "find_element_by_xpath" etc to be called as follows:
        
        self.get(url)
        self.find_element_by_xpath(query)

    with error catching and logging included.
    """
    def __init__(self, session_id):
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        """A short description of what the scraper does. This will show up as a 
        tooltip in the user interface"""
        return "A short description of what the scraper does"

    def run(self):
        try:
        """
        Scraping sequence goes here. For example:
        """
        ##########################################################
            url = "https://news.ycombinator.com/"
            self.get(url)
            elements = self.find_elements_by_class_name('storylink')
            elements_text_list = [element.text for element in elements]
            for element in elements_text_list:
                self.save(
                    'Post Title', 
                    url,
                    element)
        ##########################################################
        """
        Scraping sequence ends here.
        """
        except Exception as e:
            self.log(e)
        self.destroy()
        