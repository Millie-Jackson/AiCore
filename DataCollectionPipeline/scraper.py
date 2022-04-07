from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome()

class scraper:
    def getURL(url):
        driver.get(url)

    def getTitle():
        print(driver.title)
    
    def closeSession():
        time.sleep(3)
        driver.close()

    def getSourceCode():
        print(driver.page_source)

    def search(search_term):
        try:
            button = driver.find_element(By.ID, 'nav-searchbar-btn')
            button.click()
            try:
                search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sb")))
                try:
                    search_bar.send_keys(search_term)
                    search_bar.send_keys(Keys.RETURN) # Return = Enter
                except:
                    print("Exception: No search term input")
            except:
                print("Exception: No search bar found")
        except:
            print("Exception: No search button found")
    
    def home():
        title = driver.find_element(By.ID, 'nav-image')
        title.click()

    def findRecipeList():
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
        button.click()
    
    def acceptCookies():
        try:
            cookie_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]')
            cookie_button.click()
            print("Removed Cookies")
        except:
            print("Exeption: Didnt Find Cookie Button")

    def getRecipes():
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'index-item-container')))      
        print("Found results")
        articles = main.find_elements(By.TAG_NAME, 'li')
        print("Number of Recipes:", len(articles))

        for i in articles:
            print("Recipe:" , i.text)

    def getAllRecipePages():
        pages = []
        scraper.findRecipeList()
        page = [driver.current_url]

        #total_pages = driver.find_element(By.CLASS_NAME, 'page-text')

        total_pages = [1, 2, 3, 4, 5]

        for i in total_pages:
            current_page = driver.current_url
            url_change = "?page=" + str(i)
            next_page = current_page + url_change
            print(next_page)
            pages.append(next_page)
            print("Number of Pages:", len(pages))

scraper.getURL('https://www.pickuplimes.com/')
scraper.getTitle()
scraper.acceptCookies()
scraper.getAllRecipePages()
#scraper.getSourceCode()
#scraper.search("lemon")
#time.sleep(3)
#scraper.home()
#scraper.findRecipeList()
#scraper.getRecipes()
#scraper.getPageURL()
#time.sleep(3)
scraper.closeSession()

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
