from selenium import webdriver
import time
import datetime

def test_scrape(agent_os):
    if agent_os == 'macos':
        driver = webdriver.Chrome('./autoscrape/chromedriver')
    elif agent_os == 'windows':
        driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
    driver.get("https://news.ycombinator.com/")
    time.sleep(1)
    print("scraping https://news.ycombinator.com/")

    # username_field = driver.find_element_by_xpath('//input[@id="Email"]')
    # username_field.click()
    # username_field.send_keys(username)
    
    try:
        print("scraping...")
        posts= driver.find_elements_by_class_name("athing")
        return [post.text for post in posts]

    except Exception as e:
        print("error:",e)

    driver.close()

def timestamp():
    from datetime import datetime
    datetime.now().strftime("%Y%m%d %H:%M:%S")

if __name__ == '__main__':
    test_scrape()


