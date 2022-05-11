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

class data:
    articles = []
    count = 0
    currentURL = ""
    image_links = []
    pages = []
    recipe_details = {}
    recipeLinks = []

class scraper:
    def intitialize(self, url, search_term):
        #global_ids = scraper.getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
        data.currentURL = url
        self.getURL(data.currentURL)
        self.run()
        self.closeSession()

    def run(self):
        data.currentURL = self.findRecipeList()
        self.getAllRecipePages(data.currentURL)
        self.getRecipes(data.currentURL)
        for i in data.recipeLinks:
            data.currentURL = i
            self.makeImage(self, data.currentURL)

    def getURL(url):
        '''Navigates to a website using a url passed as a perameter.'''
        driver.get(url) 

    def getTitle():
        '''Fetches the title and prints it to screen.'''
        print(driver.title)

    def closeSession():
        '''Closes the driver after 3 seconds.'''
        time.sleep(3)
        driver.quit()

    def getSourceCode():
        '''Fetches source code for the page.'''
        print(driver.page_source)

    def search(search_term):
        '''Finds search bar, types in the search term which it takes as a perameter and clicks to navigate to the next page.'''
        try:
            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-searchbar-btn')))
            button.click()
            try:
                search_bar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "sb")))
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
        '''Finds the title and clicks it.'''
        try:
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-image')))
            title.click()
        except NoSuchElementException:
            print("Exception: Title Not Found")
        except TimeoutException:
            print("Exception: Timeout: Title")

    def findRecipeList(self):
        '''Finds the recipe tab and clicks it.'''
        try:
            button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
            button.click()
        except NoSuchElementException:
            print("Exception: Recipe List Not Found")
        except TimeoutException:
            print("Exception: Timeout: Recipe List")

    def acceptCookies():
        '''Finds the accept cookies button and clicks it.'''
        try:
            cookie_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]')))
            cookie_button.click()
            print("Removed Cookies")
        except NoSuchElementException:
            print("Exeption: Didnt Find Cookie Button")
        except TimeoutException:
            print("Timeout: Accept Cookie")

    def getRecipes(self, url):
        '''Finds the recipe container and puts all the recipes in a list.'''

        try:
            main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='index-item-container']/div/div[2]/ul"))) 
        except NoSuchElementException:
            print("Exception: Can't Find Recipe List")
        except TimeoutException: 
            print("Exception: Timeout: Can't Find Recipe List")

        data.articles = main.find_elements(By.TAG_NAME, 'li')
        for i in data.articles:
            tag = i.find_element(By.TAG_NAME, 'a')
            data.recipeLinks.append(tag.get_attribute('href'))

    def getPageURL():
        '''Returns the current page url.'''
        return driver.current_url

    def getAllRecipePages(self, url):
        '''Navigates to each recipe page by modifying the current url and stores them in a list.'''

        try:
            #total_pages = driver.find_element(By.CLASS_NAME, 'page-text') #actual
            total_pages = [1, 2, 3, 4, 5] #temp to shorten runtime
        except NoSuchElementException:
            print("Exception: Total Pages Not Found")
        except TimeoutException:
            print("Exception: Timeout: Couldn't Find Total Pages")

        for i in total_pages:
            data.currentURL = driver.current_url
            url_change = "?page=" + str(i)
            next_page = data.currentURL + url_change
            data.pages.append(next_page)

    def getUniqueID(self, url):
        '''Creates a uuid for each recipe taking a url as a perameter'''
        
        page_ID = url
        just_ID = page_ID.replace(str("https://www.pickuplimes.com/recipe/"), "")

        ids = (just_ID, uuid.uuid4())

        return ids

    def getRecipeDetails(self, url):
        self.getURL(url)

        try:
            try:    
                name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/h1'))).text
            except NoSuchElementException:
                print("Exception: Name Not Found")
                name = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Name")
                name = "N/A"  

            try:
                tag = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header-info-col"]/div/header/a[1]/div/p'))).text
            except NoSuchElementException:
                print("Exception: Tag Not Found")
                tag = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Tag")
                tag = "N/A"

            try:
                description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/span'))).text
            except NoSuchElementException:
                print("Exception: Description Not Found")
                description = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Description")
                description = "N/A"

            try:
                time_total = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[2]'))).text  
            except NoSuchElementException:
                print("Exception: Total-Time Not Found")
                time_total = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Total-Time")
                time_total = "N/A"

            try:
                time_prep = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[3]'))).text
            except NoSuchElementException:
                print("Exception: Prep-Time Not Found")
                time_pre = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Prep-Time")
                time_pre = "N/A"
            
            try:
                time_cook = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[4]'))).text
            except NoSuchElementException:
                print("Exception: Cook-Time Not Found")
                time_cook = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Cook-Time")
                time_cook = "N/A" 

            try:
                allergens = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div'))).text 
            except NoSuchElementException:
                print("Exception: Allergens Not Found")
                allergens = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Allergens")
                allergens = "N/A" 

            try: 
                swap = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div'))).text
            except NoSuchElementException:
                print("Exception: Swap Not Found")
                swap = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Swap")
                swap = "N/A" 

            try:
                free_from = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div'))).text 
            except NoSuchElementException:
                print("Exception: Free-From Not Found")
                free_from = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Free-From")
                free_from = "N/A" 

            try:
                ingredients = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]'))).text
            except NoSuchElementException:
                print("Exception: Ingredients Not Found")
                ingredients = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Ingredients")
                ingredients = "N/A"
            
            try:
                directions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol'))).text
            except NoSuchElementException:
                print("Exception: Directions Not Found")
                directions = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Directions")
                directions = "N/A"

            try:
                notes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li'))).text
            except NoSuchElementException:
                print("Exception: Notes Not Found")
                notes = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Notes")
                notes = "N/A"
            
            try:
                storage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li'))).text
            except NoSuchElementException:
                print("Exception: Storage Not Found")
                storage = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Storage")
                storage = "N/A"

            try:
                picture_main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-image-container"]/img')))
            except NoSuchElementException:
                print("Exception: Main Image Not Found")
                picture_main = "N/A"
            except TimeoutException:
                print("Exception: Timeout: Didnt Find Main Image")
                picture_main = "N/A"

        except NoSuchElementException:
            print("Exception: One Or More Data Entry Not Found")
        except TimeoutException:
            print("Exception: Timeout: Didnt Find All Data Entries")

        image_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-video"]/div[2]'))) # Find the container
        image_list = image_container.find_elements(By.XPATH, 'img') # Find the children

        for i in image_list:
            link = i.get_attribute('src')
            data.image_links.append(link)
        
        data.recipe_details = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        data.recipe_details['ID'].append(self.getUniqueID(self, url))
        data.recipe_details['Name'].append(name)
        data.recipe_details['Photo'].append(picture_main)
        data.recipe_details['Tags'].append(tag)
        data.recipe_details['Description'].append(description)
        data.recipe_details['Total Time'].append(time_total)
        data.recipe_details['Prep Time'].append(time_prep)
        data.recipe_details['Cook Time'].append(time_cook)
        data.recipe_details['Allergens'].append(allergens)
        data.recipe_details['Swaps'].append(swap)
        data.recipe_details['Free From'].append(free_from)
        data.recipe_details['Ingredients'].append(ingredients)
        data.recipe_details['Directions'].append(directions)
        data.recipe_details['Notes'].append(notes)
        data.recipe_details['Storage'].append(storage)
        data.recipe_details['Images'].append(data.image_links)
        print(data.image_links)

        self.jsonFile(self)

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
            json.dump(str(data.recipe_details), json_file)
    
    def downloadImage(url, recipeName):
        '''Creates a folder called 'images' and another with the recipe name in the path for the image files to be saved in
        Uses a try except catch as it will throw an error if the folders already exists
        Adds User-Agent Headers to bypass 403 error
        Downloads the images into the folder of that recipe name'''
        try:
            directory = "images"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Root Folder 'images' Already Exists")

        try:
            recipeDirectory = recipeName.replace(".jpg", "").replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/images"
            path = os.path.join(parent_dir, recipeDirectory)
            os.mkdir(path)
            print("Directory '% s' created" % recipeDirectory)
        except:
            print("Root Folder", recipeDirectory,  "Already Exists")
        
        try:
            # Adds headers to resolve 403 Fobidden Error
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            downloadDirectory = "images/" + recipeDirectory + "/"
            fileType = '.jpg'
            fileName = downloadDirectory + recipeName + fileType
            image = urllib.request.urlretrieve(url, fileName)
        except:
            print("Error Downloading Images")          

    def makeImage(self, url):
        '''Retrieves the ID of each image using 'getRecipeDetails()
        Removes all unecissary elements from the ID string to create a file name
        Pass the file name to 'downloadImages() to create a file'''
        self.getRecipeDetails(self, url)
        for i in data.recipe_details['Images']:
            for j in i:
                IDtoName = str(data.recipe_details['ID']).split()
                IDtoName1 = str(IDtoName[0]).replace("(", "")
                IDtoName2 = str(IDtoName1).replace("[", "")
                IDtoName3 = str(IDtoName2).replace(",", "")
                IDtoName4 = str(IDtoName3).replace("'", "")

                recipeName = IDtoName4 + "-" + str(data.count) + ".jpg"
                self.downloadImage(j, recipeName)
                data.count = data.count + 1  

#scraper.closeSession()


