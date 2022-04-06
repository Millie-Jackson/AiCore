from selenium import webdriver
from selenium.webdriver import chrome
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome()

class scraper:
    def getURL(url):
        driver.get(url)

    def getTitle():
        print(driver.title)
    
    def quit():
        time.sleep(3)
        driver.quit()

scraper.getURL('https://www.pickuplimes.com/')
scraper.getTitle()
scraper.quit()

#    def __init__(self, url, options=None):
#        self.url = url
#
#        if options:
#            self.driver = chrome(ChromeDriverManager().install(), options=options)
#            else:
#            self.driver = chrome(ChromeDriverManager().install())
#
#        self.driver.get(self.url)
#    
#    def accept_cookies(self, xpath, iframe=None):
#        try: # Incase there isnt a cookie button
#            time.sleep(10) # So the website can catch up to the bot
#
#            # If there is an iframe, remove it
#            if iframe: # iframe is the frame sometimes covering the 'Accept Cookies' button
#                self.driver.switch_to.frame(iframe)

#            cookies_button = self.driver.find_element(By.XPATH, xpath)
#            cookies_button.click()
#            time.sleep(5)
#        except:
#            print('No Cookie Button')

#    def click_search_bar(self, xpath):
#        search_bar = self.driver.find_element(By.XPATH, xpath)
#        search_bar.click()
#        return search_bar

#    def write_in_search_bar(self, text: str, xpath: str) -> None:
#        search_bar = self.click_search_bar(xpath)
#        search_bar.send_keys(text)

print("END")