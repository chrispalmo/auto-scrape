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
            table_columns = [column.text for column in self.find_elements_by_xpath("//th")]
            #get table rows
            table_rows = self.find_elements_by_xpath("//tbody/tr")
            #initialise row_dict_list
            row_dict_list = []
            #iterate over table rows, storing index
            for row_index, row in enumerate(table_rows):
                #initialise row_dict
                row_dict = {}
                #iterate over table columns, storing index
                for column_index, column in enumerate(table_columns):
                    #For first column, must get text from div class information
                    if column_index == 0:
                        element = self.find_element_by_xpath("//tr[{}]/td[{}]/div[2]/div[2]".format(row_index + 1, column_index + 1))
                        element_class = element.get_attribute("class")
                        current_recommendation = element_class.split()[2]
                        #store current recommendation in row_dict
                        row_dict.update({column: current_recommendation})
                    #if any other column index, get text straight from table/row index
                    else:
                        element_text = self.find_element_by_xpath("//tr[{}]/td[{}]".format(row_index + 1, column_index + 1)).text
                        #store element_text in row_dict
                        row_dict.update({column: element_text})
                #calculate "Buy Margin"
                try:
                    row_dict["Buy Margin"] = round(((float(row_dict["Buy Below"].replace('$', '')) - float(row_dict["Current Price"].replace('$', ''))) / float(row_dict["Buy Below"].replace('$', ''))) * 100, 2)
                except ValueError:
                    row_dict["Buy Margin"] = 0
                #calculate "Sell Margin"
                try:
                    row_dict["Sell Margin"] = round(((float(row_dict["Sell Above"].replace('$', '')) - float(row_dict["Current Price"].replace('$', ''))) / float(row_dict["Sell Above"].replace('$', ''))) * 100, 2)
                except ValueError:
                    row_dict["Sell Margin"] = 0
                #append row_dict to row_dict_list with each row iteration
                row_dict_list.append(row_dict)
            for row in row_dict_list:
                print(row)
            self.destroy()

        except Exception as e:
            self.log(e)
            self.destroy()


"""
#get column headings
table_columns = [column.text for column in driver.find_elements_by_xpath("//th")]
#get table rows
table_rows = driver.find_elements_by_xpath("//tbody/tr")
#initialise row_dict_list
row_dict_list = []
#iterate over table rows
for row_index, row in enumerate(table_rows):
    row_dict = {}
    for column_index, column in enumerate(table_columns):
        if column_index == 0:
            element = driver.find_element_by_xpath("//tr[{}]/td[{}]/div[2]/div[2]".format(row_index+1, column_index+1))
            element_class = element.get_attribute("class")
            current_recommendation = element_class.split()[2]
            row_dict.update({column: current_recommendation})
        else:
            element_text = driver.find_element_by_xpath("//tr[{}]/td[{}]".format(row_index+1, column_index+1)).text
            row_dict.update({column: element_text})
    row_dict_list.append(row_dict)
"""