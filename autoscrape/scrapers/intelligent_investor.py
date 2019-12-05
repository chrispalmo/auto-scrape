from threading import Thread
from autoscrape import base_scraper
from os import environ


class IntelligentInvestor(Thread, base_scraper.Scraper):

    def __init__(self, session_id):
        Thread.__init__(self)
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        return "Intelligent Investor Scraper"

    def run(self):
        # Scraping sequence goes here. Logging is taken care of by the base_scraper base class for standard browser functions.
        try:
            # Get recommendations
            url = "https://www.intelligentinvestor.com.au/identity/logon?returnUrl=%2Fresearch%2Frecommendations&prefix=2"
            self.get(url)
            login_form = self.driver.find_element_by_xpath("//input[@id='Email']")
            login_form.click()
            login_form.send_keys(environ['USERNAME'])
            password_form = self.driver.find_element_by_xpath("//input[@id='Password']")
            password_form.click()
            password_form.send_keys(environ['PASSWORD'])
            login_button = self.driver.find_element_by_xpath("//input[contains(@class, 'btn btn-primary btn-fw btn-brand-style-with-pad')]")
            login_button.click()
            result_dropdown = self.driver.find_element_by_xpath("//button[contains(@class, 'btn btn-default dropdown-toggle ng-binding')]")
            result_dropdown.click()
            result_dropdown_250 = self.driver.find_element_by_xpath("//ul[contains(@class, 'dropdown-menu')]/li[contains(@class, 'ng-scope')][4]/a[contains(@class, 'ng-binding')]")
            result_dropdown_250.click()
        except Exception as e:
            self.log(e)