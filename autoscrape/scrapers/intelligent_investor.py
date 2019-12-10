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
            #enter email address
            login_email_form = self.find_element_by_xpath("//input[@id='Email']")
            login_email_form.click()
            login_email_form.send_keys(environ['USERNAME'])
            #enter password
            login_password_form = self.find_element_by_xpath("//input[@id='Password']")
            login_password_form.click()
            login_password_form.send_keys(environ['PASSWORD'])
            #submit form
            login_submit_button = self.find_element_by_xpath("//input[contains(@class, 'btn btn-primary btn-fw btn-brand-style-with-pad')]")
            login_submit_button.click()
            #increase results on page
            result_dropdown = self.find_element_by_xpath("//button[contains(@class, 'btn btn-default dropdown-toggle ng-binding')]")
            result_dropdown.click()
            result_dropdown_250 = self.find_element_by_xpath("//ul[contains(@class, 'dropdown-menu')]/li[contains(@class, 'ng-scope')][4]/a[contains(@class, 'ng-binding')]")
            result_dropdown_250.click()
            #get column headings
            table_columns = self.find_elements_by_xpath("//th")
            #get table rows
            table_rows = self.find_elements_by_xpath("//tbody/tr")
            #initialise row_dict and row_dict_list
            row_dict_list = []
            row_dict = {}
            for row in table_rows:
                for column in table_columns:
                    print("Scraping row {}, column {}".format(table_rows.index(row) +1, table_columns.index(column) + 1))
                    row_dict.update({column.text: self.find_element_by_xpath("//tr[{}]/td[{}]".format(table_rows.index(row) + 1, table_columns.index(column) + 1)).text})
                    row_dict_list.append(row_dict)
            return row_dict_list
        except Exception as e:
            self.log(e)

        self.destroy()