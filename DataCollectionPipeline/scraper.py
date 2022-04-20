from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

import time
import uuid

driver = webdriver.Chrome()

class scraper:
    def intitialize(self, url, search_term):
        #global_ids = scraper.getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
        self.getURL()
        #self.getTitle()
        #self.acceptCookies()
        #self.getAllRecipePages()
        #self.getSourceCode()
        #self.search(search_term)
        #time.sleep(3)
        #self.home()
        #self.findRecipeList()
        #self.getRecipes()
        #self.getPageURL()
        self.getRecipeDetails(self)
        #time.sleep(3)
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
            except NoSuchElementException:
                print("Exception: No search bar found")
        except TimeoutException:
            print("Exception: Timeout: Search bar"))
    
    def home():
        try:
            title = driver.find_element(By.ID, 'nav-image')
            title.click()
        except NoSuchElementException:
            print("Exception: Title Not Found")
        except TimeoutException:
            print("Exception: Timeout: Title")

    def findRecipeList():
        try:
            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
            button.click()
        except NoSuchElementException:
            print("Exception: Recipe List Not Found")
        except TimeoutException:
            print("Exception: Timeout: Recipe List")
    
    def acceptCookies():
        try:
            cookie_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]')
            cookie_button.click()
            print("Removed Cookies")
        except NoSuchElementException:
            print("Exeption: Didnt Find Cookie Button")
        except TimeoutException:
            print("Timeout: Accept Cookie")

    def getRecipes():
        try:
            main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'index-item-container')))      
            articles = main.find_elements(By.TAG_NAME, 'li')
            print("Number of Recipes:", len(articles))
        except NoSuchElementException:
            print("Exception: Can't Find Recipe List")
        except TimeoutException: 
            print("Exception: Timeout: Can't Find Recipe List")

        for i in articles:
            print("Recipe:" , i.text)

    def getAllRecipePages(self):
        pages = []
        self.getURL('https://www.pickuplimes.com/')
        scraper.findRecipeList()
        page = [driver.current_url]

        try:
            #total_pages = driver.find_element(By.CLASS_NAME, 'page-text') #actual
            total_pages = [1, 2, 3, 4, 5] #temp to shorten runtime
        except NoSuchElementException:
            print("Exception: Total Pages Not Found")
        except TimeoutException:
            print("Exception: Timeout: Couldn't Find Total Pages")

        for i in total_pages:
            current_page = driver.current_url
            url_change = "?page=" + str(i)
            next_page = current_page + url_change
            print(next_page)
            pages.append(next_page)
            print("Number of Pages:", len(pages))

    def getUniqueID(self, url):
        
        page_ID = url
        just_ID = page_ID.replace(str("https://www.pickuplimes.com/recipe/"), "")

        ids = (just_ID, uuid.uuid4())

        return ids

    def getRecipeDetails(self):
        self.getURL('https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')

        try:
            name = driver.find_element(By.XPATH, '//*[@id="header-info-col"]/div/header/h1').text
            tag = driver.find_element(By.XPATH, '//*[@id="header-info-col"]/div/header/a[1]/div/p').text
            description = driver.find_element(By.XPATH, '//*[@id="header-info-col"]/div/header/span').text
            time_total = driver.find_element(By.XPATH, '//*[@id="recipe-info-container"]/div[2]').text
            time_prep = driver.find_element(By.XPATH, '//*[@id="recipe-info-container"]/div[3]').text
            time_cook = driver.find_element(By.XPATH, '//*[@id="recipe-info-container"]/div[4]').text
            allergens = driver.find_element(By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div').text 
            swap = driver.find_element(By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div').text
            free_from = driver.find_element(By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div').text  
            ingredients = driver.find_element(By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]').text
            directions = driver.find_element(By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol').text
            notes = driver.find_element(By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li').text
            storage = driver.find_element(By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li').text
            picture_main = driver.find_element(By.XPATH, '//*[@id="main-image-container"]/img')
        except NoSuchElementException:
            print("Exception: One Or More Data Entry Not Found")
        except TimeoutException:
            print("Exception: Timeout: Didnt Find All Data Entries")

        image_container = driver.find_element(By.XPATH, '//*[@id="recipe-video"]/div[2]') # Find the container
        image_list = image_container.find_elements(By.XPATH, 'img') # Find the children
        print(len(image_list))
        image_links= []

        for i in image_list:
            link = i.get_attribute('src')
            image_links.append(link)
        
        recipe_details = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        recipe_details['ID'].append(self.getUniqueID(self, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213'))
        recipe_details['Name'].append(name)
        recipe_details['Photo'].append(picture_main)
        recipe_details['Tags'].append(tag)
        recipe_details['Description'].append(description)
        recipe_details['Total Time'].append(time_total)
        recipe_details['Prep Time'].append(time_prep)
        recipe_details['Cook Time'].append(time_cook)
        recipe_details['Allergens'].append(allergens)
        recipe_details['Swaps'].append(swap)
        recipe_details['Free From'].append(free_from)
        recipe_details['Ingredients'].append(ingredients)
        recipe_details['Directions'].append(directions)
        recipe_details['Notes'].append(notes)
        recipe_details['Storage'].append(storage)
        recipe_details['Images'].append(image_list)

scraper.getRecipeDetails(scraper)

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
