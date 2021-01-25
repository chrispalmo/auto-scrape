from autoscrape import base_scraper
from os import environ
import requests
import time
from autoscrape.helpers import to_filename
from selenium.webdriver.common.keys import Keys


class PyImageSearch(base_scraper.Scraper):

    def __init__(self, session_id):
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        return "Save course code for tutorials on pyimagesearch.mykajabi.com"

    def run(self):
        try:
            url = "https://pyimagesearch.mykajabi.com/login"
            self.get(url)
            """
            Login form
            """
            try:
                username = environ['PYIMAGESEARCH_EMAIL']
                password = environ['PYIMAGESEARCH_PASSWORD']
            except KeyError as e:
                self.log("Username or Password not provided. Contact system administrator to ensure they have been provided as environment variables.")
                raise
            login_email_form = self.find_element_by_xpath("//input[@id='member_email']")
            login_email_form.click()
            login_email_form.send_keys(username)
            login_password_form = self.find_element_by_xpath("//input[@id='member_password']")
            login_password_form.click()
            login_password_form.send_keys(password)
            login_submit_button = self.find_element_by_xpath("//input[@class='btn btn--block btn--solid btn--med']")
            login_submit_button.click()
            """
            Go to downloads page
            """
            url = "https://pyimagesearch.mykajabi.com/products/pyimagesearch-plus-basic-code-plan/categories/3987599/posts/13369975"
            self.get(url)
            """
            Scrape!
            """
            # container to iterate over
            for i in range(4,294):
                title = self.find_element_by_xpath(f"//div[@class='panel__block']/p[{i}]/strong").text
                download_link = self.find_element_by_xpath(f"//div[@class='panel__block']/p[{i}]/a")
                download_url = download_link.get_attribute("href")
                self.log(title)
                self.log(download_url)
                # download_link.click()
                self.save("download link", download_url, title + "; " + download_url.split("/")[-1])
                time.sleep(1)
            self.destroy()
        except Exception as e:
            self.log(e)
            self.destroy(completed=False)
            raise