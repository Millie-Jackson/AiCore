import requests
import urllib
import time
import uuid
import json
import os

from uuid import UUID
from json import JSONEncoder
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()

class scraper:
    def intitialize(self, url, search_term, delay):
        global_ids = scraper.getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
        
        self.getURL(url)
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
        #self.getUniqueID()
        #self.getRecipeDetails(self)
        #self.jsonFile() # Could be private?
        #self.downloadImage('/html/body/img', 'nameForImage') # Could be private?
        self.getImages(self, 'https://www.pickuplimes.com/recipe/harissa-spiced-beans-898')
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
            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-searchbar-btn')))
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
            print("Exception: Timeout: Search bar")
    
    def home():
        try:
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-image')))
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
            cookie_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]')))
            cookie_button.click()
            print("Removed Cookies")
        except NoSuchElementException:
            print("Exeption: Didnt Find Cookie Button")
        except TimeoutException:
            print("Timeout: Accept Cookie")

    def getRecipes():
        try:
            main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'index-item-container')))      
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
            name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/h1'))).text
            tag = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header-info-col"]/div/header/a[1]/div/p'))).text
            description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/span'))).text
            time_total = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[2]'))).text  
            time_prep = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[3]'))).text
            time_cook = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[4]'))).text
            allergens = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div'))).text 
            swap = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div'))).text
            free_from = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div'))).text  
            ingredients = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]'))).text
            directions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol'))).text
            notes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li'))).text
            storage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li'))).text
            picture_main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-image-container"]/img')))
        except NoSuchElementException:
            print("Exception: One Or More Data Entry Not Found")
        except TimeoutException:
            print("Exception: Timeout: Didnt Find All Data Entries")

        image_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-video"]/div[2]'))) # Find the container
        image_list = image_container.find_elements(By.XPATH, 'img') # Find the children
        print(len(image_list))
        image_links= []

        for i in image_list:
            link = i.get_attribute('src')
            image_links.append(link)
        
        self.recipe_details = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        self.recipe_details['ID'].append(self.getUniqueID(self, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213'))
        self.recipe_details['Name'].append(name)
        self.recipe_details['Photo'].append(picture_main)
        self.recipe_details['Tags'].append(tag)
        self.recipe_details['Description'].append(description)
        self.recipe_details['Total Time'].append(time_total)
        self.recipe_details['Prep Time'].append(time_prep)
        self.recipe_details['Cook Time'].append(time_cook)
        self.recipe_details['Allergens'].append(allergens)
        self.recipe_details['Swaps'].append(swap)
        self.recipe_details['Free From'].append(free_from)
        self.recipe_details['Ingredients'].append(ingredients)
        self.recipe_details['Directions'].append(directions)
        self.recipe_details['Notes'].append(notes)
        self.recipe_details['Storage'].append(storage)
        self.recipe_details['Images'].append(image_links)

        self.jsonFile(self)

    '''This function creates a folder for all the data then creates a json file and writes the data dictionary to it'''
    def jsonFile(self):
        '''Creates a folder called 'raw_data' in the path for the json file to be saved in
        Uses a try except catch as it will throw an error if the folder already exists'''
        try:
            directory = "raw_data"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Root Folder 'raw_data' Already Exists")

        '''Deals with TypeError: Object of type UUID is not JSON serializable by encoding the UUID'''
        JSONEncoder_olddefault = JSONEncoder.default
        def JSONEncoder_newdefault(self, o):
            if isinstance(o, UUID): return str(o)
            return JSONEncoder_olddefault(self, o)
        JSONEncoder.default = JSONEncoder_newdefault

        '''Stores data by writing the 'recipe_details' dictionary to a JSON file called 'data.json' in the folder just created
        The dicrionary is converted to a string using str() to deal with 'TypeError: Object of type WebElement is not JSON serializable'''
        with open(os.path.join('raw_data', 'data.json'), 'w') as json_file:
            json.dump(str(self.recipe_details), json_file)

    def downloadImage(url, recipeName):
        '''Creates a folder called 'images' in the path for the image files to be saved in
        Uses a try except catch as it will throw an error if the folder already exists
        Adds User-Agent Headers to bypass 403 error
        Downloads an image into the images folder'''
        try:
            directory = "images"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Root Folder 'images' Already Exists")
        
        try:
            # Adds headers to resolve 403 Fobidden Error
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            directory = "images/"
            fileType = '.jpg'
            fileName = directory + recipeName + fileType
            image = urllib.request.urlretrieve(url, fileName)
        except:
            print("Error Downloading Image")           

    def getImages(self, url):
        '''Retrieves the ID of each image using 'getRecipeDetails()
        Removes all unecissary elements from the ID string to create a file name
        Pass the file name to 'downloadImages() to create a file'''

        self.getRecipeDetails(self)
        for i in self.recipe_details['Images']:
            for j in i:
                IDtoName = str(self.recipe_details['ID']).split()
                IDtoName1 = str(IDtoName[0]).replace("(", "")
                IDtoName2 = str(IDtoName1).replace("[", "")
                IDtoName3 = str(IDtoName2).replace(",", "")
                IDtoName4 = str(IDtoName3).replace("'", "")

                self.downloadImage(j, IDtoName4)

scraper.getImages(scraper, 'https://www.pickuplimes.com/recipe/harissa-spiced-beans-898')

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
