from selenium import webdriver
import time
import datetime

def test_scrape():
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get("https://news.ycombinator.com/")
    time.sleep(1)
    print("scraping https://news.ycombinator.com/")

    # username_field = driver.find_element_by_xpath('//input[@id="Email"]')
    # username_field.click()
    # username_field.send_keys(username)
    
    try:
        print("scraping...")
        posts= driver.find_element_by_class_name("athing").text
        print(posts)
        return posts

    except Exception as e:
        print("error:",e)

    driver.close()

def timestamp():
    from datetime import datetime
    datetime.now().strftime("%Y%m%d %H:%M:%S")

if __name__ == '__main__':
    test_scrape()


