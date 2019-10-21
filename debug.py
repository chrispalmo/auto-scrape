from selenium import webdriver

'''
How to use:

1. Open python
2. from debug import driver
3. driver.get(url)
'''

agent_os = input("Are you using Windows operating system? [Y/N] Default: [N] >>>")
if (agent_os == 'y') or (agent_os) == 'Y':
	driver = webdriver.Chrome('./autoscrape/chromedriver.exe')
else:
	driver = webdriver.Chrome('./autoscrape/chromedriver')