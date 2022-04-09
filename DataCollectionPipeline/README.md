DESCRIPTION
A webscraper that runs of the recipe website 'Pick Up Limes'. The goal is to scraping and comparing recipies with similar names from more than one site in order to create a 'master' copy of common recipes detailing essential and optional ingrediants rather than having multiple varients of the same recipe. This website was used for its user friendly simplicity and decent amount of data to crawl. The topic is also relivant and useful to the industry as cooking is a part of everyday life and specifically veganism has become popular recently. This model would be valuable for those in the industry looking to reduce the psychological concept of decision fatuigue which is a well established issue in marketing/advertising/retail, and also for individual use who want to simplyfy their cooking/lifestyle.

It would be ideal if the model could take in a list of ingrediants (and kitchen tools) available in an individuals home and make suggestions on what meals could be made using whats currently available. Profiles could than be used within a app using common profile, diatry and lifestyle options

WEBSITES
- pickuplimes.com 
    - author is a dietician and influencer
    - recipes are designed to be simple and maximise nutrition
- avantguardevegan.com 
    - author is a chef and influencer
    - recipes are on the more 'advanced' and complicated side

The contents for both sites where chosen because they compliment each other, ranging from 'easy to advanced' and 'practical to one-off-events'. There are multiple recipes for the same dish for comparison.

TECHNOLOGY 
Used:
- Python:        
    -commonly used for web scraping and data crawling
- Requests:       
    - chosen for its various options to access html elements and was found to have more prectical to use than BeautifulSoup. 
    - it can also be used on multiple sites at once
- Selenium:
    - it is a popular freeware automation tool, its also open source and has good documentaion.
    - it can also run multiple scripts on multiple urls at once which matched the end goal of scraping and comparing recipies with similar names from more than one site
- Chrome Driver:
    - chrome is the dominant browser
- VSCode:
    - an industry standard and great pairing for Python
- GutHub:
    - industry standard and was used for its version control

MILESTONE 1

FEATURES:
Scraper Class:
    - a script containing all methods used for scraping
    - imports and initializes in the main code
    - successfully scrapes from 'Pick Up Limes'
    - uses a if __name__ == "__main__" guard
Navigation:
    - uses url as an argument to navigate to the website
    - finds and clicks a button
    - finds the recipe tab by LINK_NAME and loads it
    - Extra: finds the title and uses it to navigate back to the home screen
    - Extra: finds the search bar and uses a search term passed as an arguments to navigate to specific recipes
    - Extra: closes or quits using a method instead of the driver
Specific: 
    - finds cookie button and clickes it to remove (there is no iframe on this website), uses a try statement to catch exceptions incase there is no cookie button
Scraping:
    - gets the url (when navigating to a specific page or storing recipe pages for later use)
    - finds the first page of recipes, returnes the url and modifies it in order to predict the 
    next page url. Each url is then stored in a list which displays its size. Currently capped at 5 as there is it cant detect how many total pages there are on a site
    - Extra: gets the websites source code
    - Extra: gets the title (to be used when navigating home)
    - Extra: counts how many recipes are on that page and displays the titles

CODE
-----------------------------------------------------------------------
from scraper import scraper
import time

bot = scraper()

if __name__ == "__main__":
    bot.intitialize(bot, 'https://www.pickuplimes.com/', 'lemons')
else:
    print("Error: Driver closed because of initialize")
    bot.close()
-----------------------------------------------------------------------
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
    def intitialize(self, url, search_term):
        self.getURL(url)
        self.getTitle()
        self.acceptCookies()
        self.getAllRecipePages()
        self.getSourceCode()
        self.search(search_term)
        time.sleep(3)
        self.home()
        self.findRecipeList()
        self.getRecipes()
        self.getPageURL()
        time.sleep(3)
        self.closeSession()

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
-----------------------------------------------------------------------