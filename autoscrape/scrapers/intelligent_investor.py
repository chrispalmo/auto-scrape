from autoscrape import base_scraper
from os import environ
import time


class IntelligentInvestor(base_scraper.Scraper):

    def __init__(self, session_id):
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        return "Intelligent Investor Scraper"

    def run(self):
        try:
            url = "https://www.intelligentinvestor.com.au/identity/logon?returnUrl=%2Fresearch%2Frecommendations&prefix=2"
            self.get(url)
            time.sleep(2)
            """
            Login form
            """
            try:
                username = environ['II_USERNAME']
                password = environ['II_PASSWORD']
            except KeyError as e:
                self.log("Username and Password not provided. Contact system administrator to ensure they have been provided as environment variables.")
                raise
            login_email_form = self.find_element_by_xpath("//input[@id='Email']")
            login_email_form.click()
            login_email_form.send_keys(username)
            login_password_form = self.find_element_by_xpath("//input[@id='Password']")
            login_password_form.click()
            login_password_form.send_keys(password)
            login_submit_button = self.find_element_by_xpath("//input[contains(@class, 'btn btn-primary btn-fw btn-brand-style-with-pad')]")
            login_submit_button.click()
            time.sleep(2)
            """
            Increase result count on page
            """
            result_dropdown = self.find_element_by_xpath("//button[contains(@class, 'btn btn-default dropdown-toggle ng-binding')]")
            result_dropdown.click()
            result_dropdown_250 = self.find_element_by_xpath("//ul[contains(@class, 'dropdown-menu')]/li[contains(@class, 'ng-scope')][4]/a[contains(@class, 'ng-binding')]")
            result_dropdown_250.click()
            time.sleep(2)
            """
            Get table column/row indexes
            """
            table_columns = [column.text for column in self.find_elements_by_xpath("//th")]
            table_rows_count = len(self.find_elements_by_xpath("//tbody/tr"))
            """
            Scrape table data
            """
            row_dict_list = []
            for row_index in range(table_rows_count):
                row_dict = {}
                for column_index, column in enumerate(table_columns):
                    if column_index == 0:
                        element = self.find_element_by_xpath("//tr[{}]/td[{}]/div[2]/div[2]".format(row_index + 1, column_index + 1))
                        element_class = element.get_attribute("class")
                        current_recommendation = element_class.split()[2]
                        row_dict.update({column: str(current_recommendation)})
                    else:
                        element_text = self.find_element_by_xpath("//tr[{}]/td[{}]".format(row_index + 1, column_index + 1)).text
                        row_dict.update({column: str(element_text)})
                """
                Calculate "Buy Margin" and "Sell Margin" 
                """
                buy_below = None
                sell_above = None
                current_price = None
                try:
                    buy_below = float(row_dict["Buy Below"].replace('$', ''))
                    sell_above = float(row_dict["Sell Above"].replace('$', ''))
                    current_price = float(row_dict["Current Price"].replace('$', ''))
                except ValueError:
                    pass
                try:
                    row_dict["Buy Margin"] = str(round(((buy_below - current_price) / buy_below) * 100, 2))
                except TypeError:
                    row_dict["Buy Margin"] = "-"
                try:
                    row_dict["Sell Margin"] = str(round(((current_price - sell_above) / sell_above) * 100, 2))
                except TypeError:
                    row_dict["Sell Margin"] = "-"
                """
                Build final list of dictionaries
                """
                row_dict_list.append(row_dict)
            """
            Modify data format and write to database
            """
            column_string = ';'.join(row_dict_list[0].keys())
            self.save("headings", url, column_string)
            for row_dict in row_dict_list:
                row_string = ';'.join(row_dict.values())
                self.save("recommendation", url, row_string)
            self.destroy()
        except Exception as e:
            self.destroy(completed=False)
            raise