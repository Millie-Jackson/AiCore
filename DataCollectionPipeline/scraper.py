import functools # used to maintain introspection on decorators
import requests
import urllib
import time
import uuid # used to create a unique 'computer' id for each recipe
import json # used to store the scraped details
import os

from uuid import UUID # used to create a unique id for each recipe
from json import JSONEncoder # used to convert the UUID into a writable format
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

    articles = [] # Used to make a list of recipes
    button = None # Used to interact with various button elements
    container = None # Used to store various container elements
    currentURL = "" # Used to store various urls 
    pages = [] # Used to append a list with pages links
    recipeLinks = [] # Used to store recipe links
    recipeName = "" # Stores the recipe name
    searchbar = None # Used to interact with search bar
    source = "" # Used to get page source code
    tag = None # Used to store various tag elements
    title = "" # Used to get the title
    totalPages = [] # Stores a list of pages

    # File Management
    count = 0 # Used in the creation of image filenames
    dataDirectory = "" # Used to create folder
    imageDirectory = "" # Used to create folder 
    recipeDirectory = "" # Used to create modified folder names

    # Scraped Information
    recipeDetails = {} # Used to store all the scraped recipe details

    allergens = "" # Used to store scraped allergens
    alternatives = "" #Used to store scraped alternatives
    description = "" # Used to store the scraped description of the recipe
    freeFrom = "" # Used to store the scraped free from information
    imageLinks = [] # Used to scrape all of a recipes image links
    ingredients = "" # Used to store the scraped ingredients
    instructions = "" # Used to store scraped instructions
    mainPhoto = None # Used to store main photo link
    name = "" # Used to store scraped recipe name
    notes = "" # Used to store scraped recipe notes
    recipeTags = "" # Used to store scraped recipe tags
    storage = "" # Used to store scraped storage instructions
    timeCook = "" # Used to store scraped cook time
    timePrep = "" # Used to store scraped recipe  prep time 
    timeTotal = "" # Used to store scraped total time it takes to make the recipe

class scraper:
    def intitialize(self, url, searchTerm):
        global_ids = scraper.getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
    
        self.getURL(self, url) # Have to start somewhere
        self.run(self)
        self.closeSession() # Have to end somewhere
        
    
    # DECORATORS

    def exceptionHandling(func):
        @functools.wraps(func) # maintains introspection
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except NoSuchElementException:
                print(f"{func.__name__} Exception: Element Not Found")
            except TimeoutException:
                print(f"{func.__name__} Exception: Timeout")
            return func(*args, **kwargs)
        return wrapper


    def run(self) -> None:
        #self.acceptCookies()
        data.currentURL = self.findRecipeList(self)
        self.getAllRecipePages(self, data.currentURL)
        self.getRecipes(self, data.currentURL)
        self.cycleRecipeLinks(self)
        self.closeSession()   

    def cycleRecipeLinks(self) -> None:
        for i in data.recipeLinks:
            data.currentURL = i
            self.makeImage(self, data.currentURL)

    def getURL(self, url) -> None:
        '''Navigates to a website using a url passed as a perameter.'''
        driver.get(url) 

    def getTitle() -> None:
        '''Fetches the title and prints it to screen.'''
        data.title = driver.title

    def closeSession() -> None:
        '''Closes the driver'''
        driver.quit()

    def getSourceCode() -> None:
        '''Fetches source code for the page.'''
        data.source = driver.page_source

    @exceptionHandling
    def search(self, searchTerm) -> None:
        '''Finds search bar, types in the search term which it takes as a perameter and clicks to navigate to the next page.'''
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-searchbar-btn')))
        button.click()

        self.findSearchbar(self, searchTerm)

    def searchbarTextAndClick(searchTerm) -> None:
        try:
            data.searchbar.send_keys(searchTerm)
            data.searchbar.send_keys(Keys.RETURN) # Return = Enter
        except:
            print("Exception: No search term input")
    
    @exceptionHandling
    def findSearchbar(self, searchTerm) -> None:

        data.searchbar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "sb")))
        self.searchbarTextAndClick(searchTerm)

    @exceptionHandling
    def home() -> None:
        '''Finds the title and clicks it.'''
        title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-image')))
        title.click()

    @exceptionHandling
    def findRecipeList(self):
        '''Finds the recipe tab and clicks it.'''
        data.button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
        data.button.click()

    @exceptionHandling
    def acceptCookies() -> None:
        '''Finds the accept cookies button and clicks it.'''
        data.button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]')))
        data.button.click()
    
    def getRecipes(self, url) -> None:
        '''Finds the recipe container and puts all the recipes in a list.'''

        self.getRecipeContainer()
        self.makeRecipeList()

    @exceptionHandling
    def getRecipeContainer() -> None:
        data.container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='index-item-container']/div/div[2]/ul"))) 

    def makeRecipeList() -> None:
        data.articles = data.container.find_elements(By.TAG_NAME, 'li')

        for i in data.articles:
            data.tag = i.find_element(By.TAG_NAME, 'a')
            data.recipeLinks.append(data.tag.get_attribute('href'))

    def getPageURL() -> None:
        '''Returns the current page url.'''
        data.currentURL =  driver.current_url

    def getAllRecipePages(self, url) -> None:
        '''Navigates to each recipe page by modifying the current url and stores them in a list.'''

        self.getTotalPages()
        self.getSearchList()

    @exceptionHandling
    def getTotalPages() -> None:
         #totalPages = driver.find_element(By.CLASS_NAME, 'page-text') #actual
        data.totalPages = [1, 2, 3] #temp to shorten runtime

    def getSearchList() -> None:
        for i in data.totalPages:
            data.currentURL = driver.current_url
            url_change = "?page=" + str(i)
            next_page = data.currentURL + url_change
            data.pages.append(next_page)

    def getUniqueID(self, url) -> None:
        '''Creates a uuid for each recipe taking a url as a perameter'''
        
        page_ID = url
        just_ID = page_ID.replace(str("https://www.pickuplimes.com/recipe/"), "")

        ids = (just_ID, uuid.uuid4())

    def scrapeName() -> None:
        try:    
            data.name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/h1'))).text
        except NoSuchElementException:
            print("Exception: Name Not Found")
            data.name = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Name")
            data.name = "N/A" 

    def scrapeTags() -> None:
        try:
            data.recipeTags = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header-info-col"]/div/header/a[1]/div/p'))).text
        except NoSuchElementException:
            print("Exception: Tag Not Found")
            data.recipeTags = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Tag")
            data.recipeTags = "N/A"

    def scrapeDescription() -> None:
        try:
            data.description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/span'))).text
        except NoSuchElementException:
            print("Exception: Description Not Found")
            data.description = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Description")
            data.description = "N/A"

    def scrapeTotalTime() -> None:
        try:
            data.timeTotal = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[2]'))).text  
        except NoSuchElementException:
            print("Exception: Total-Time Not Found")
            data.timeTotal = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Total-Time")
            data.timeTotal = "N/A"

    def scrapePrepTime() -> None:
        try:
            data.timePrep = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[3]'))).text
        except NoSuchElementException:
            print("Exception: Prep-Time Not Found")
            data.timePrep = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Prep-Time")
            data.timePrep = "N/A"

    def scrapeCookTime() -> None:
        try:
            data.timeCook = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[4]'))).text
        except NoSuchElementException:
            print("Exception: Cook-Time Not Found")
            data.timeCook = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Cook-Time")
            data.timeCook = "N/A" 

    def scrapeAllergens() -> None:
        try:
            data.allergens = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div'))).text 
        except NoSuchElementException:
            print("Exception: Allergens Not Found")
            data.allergens = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Allergens")
            data.allergens = "N/A"

    def scrapeAlternatives() -> None:
        try: 
            data.alternatives = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div'))).text
        except NoSuchElementException:
            print("Exception: Swap Not Found")
            data.alternatives = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Swap")
            data.alternatives = "N/A"

    def scrapeFreeFrom() -> None:
        try:
            data.freeFrom = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div'))).text 
        except NoSuchElementException:
            print("Exception: Free-From Not Found")
            data.freeFrom = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Free-From")
            data.freeFrom = "N/A" 

    def scrapeIngredients() -> None:
        try:
            data.ingredients = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]'))).text
        except NoSuchElementException:
            print("Exception: Ingredients Not Found")
            data.ingredients = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Ingredients")
            data.ingredients = "N/A"

    def scrapeInstructions() -> None:
        try:
            data.instructions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol'))).text
        except NoSuchElementException:
            print("Exception: Directions Not Found")
            data.instructions = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Directions")
            data.instructions = "N/A"

    def scrapeNotes() -> None:
        try:
            data.notes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li'))).text
        except NoSuchElementException:
            print("Exception: Notes Not Found")
            data.notes = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Notes")
            data.notes = "N/A"

    def scrapeStorage() -> None:
        try:
            data.storage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li'))).text
        except NoSuchElementException:
            print("Exception: Storage Not Found")
            data.storage = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Storage")
            data.storage = "N/A"

    def scrapeMainPhoto() -> None:
        try:
            data.mainPhoto = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-image-container"]/img')))
        except NoSuchElementException:
            print("Exception: Main Image Not Found")
            data.mainPhoto = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Main Image")
            data.mainPhoto = "N/A"

    @exceptionHandling
    def scrapeImages() -> None:
        imageContainer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-video"]/div[2]'))) # Find the container
        imageList = imageContainer.find_elements(By.XPATH, 'img') # Find the children

        for i in imageList:
            link = i.get_attribute('src')
            data.imageLinks.append(link)

    @exceptionHandling
    def getRecipeDetails(self, url) -> None:
        self.getURL(url)

        self.scrapeName()  
        self.scrapeTags()
        self.scrapeDescription()
        self.scrapeTotalTime()
        self.scrapePrepTime()
        self.scrapeCookTime()
        self.scrapeAllergens()
        self.scrapeAlternatives()
        self.scrapeFreeFrom()
        self.scrapeIngredients()
        self.scrapeInstructions()
        self.scrapeNotes()
        self.scrapeStorage()
        self.scrapeMainPhoto()
        self.scrapeImages()

        self.storeDetails(self, url)
        self.jsonFile(self)

    def storeDetails(self, url) -> None:
        data.recipeDetails = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        data.recipeDetails['ID'].append(self.getUniqueID(self, url))
        data.recipeDetails['Name'].append(data.name)
        data.recipeDetails['Photo'].append(data.mainPhoto)
        data.recipeDetails['Tags'].append(data.recipeTags)
        data.recipeDetails['Description'].append(data.description)
        data.recipeDetails['Total Time'].append(data.timeTotal)
        data.recipeDetails['Prep Time'].append(data.timePrep)
        data.recipeDetails['Cook Time'].append(data.timeCook)
        data.recipeDetails['Allergens'].append(data.allergens)
        data.recipeDetails['Swaps'].append(data.alternatives)
        data.recipeDetails['Free From'].append(data.freeFrom)
        data.recipeDetails['Ingredients'].append(data.ingredients)
        data.recipeDetails['Directions'].append(data.instructions)
        data.recipeDetails['Notes'].append(data.notes)
        data.recipeDetails['Storage'].append(data.storage)
        data.recipeDetails['Images'].append(data.imageLinks)

    def jsonFile(self) -> None:
        '''Creates a folder called 'raw_data' in the path for the json file to be saved in
        Uses a try except catch as it will throw an error if the folder already exists'''

        self.makeRaw_DataFolder()

        '''Deals with TypeError: Object of type UUID is not JSON serializable by encoding the UUID'''
        JSONEncoder_olddefault = JSONEncoder.default
        def JSONEncoder_newdefault(self, o):
            if isinstance(o, UUID): return str(o)
            return JSONEncoder_olddefault(self, o)
        JSONEncoder.default = JSONEncoder_newdefault

        self.jsonDump()

    def makeRaw_DataFolder() -> None:
        try:
            directory = "raw_data"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Folder already exists: raw_data")
    
    def jsonDump() -> None:
        '''Stores data by writing the 'recipe_details' dictionary to a JSON file called 'data.json' in the folder just created
        The dicrionary is converted to a string using str() to deal with 'TypeError: Object of type WebElement is not JSON serializable'''
        with open(os.path.join('raw_data', 'data.json'), 'w') as json_file:
            json.dump(str(data.recipeDetails), json_file)

    def downloadImage(self, url, recipeName) -> None:
        '''Creates a folder called 'images' and another with the recipe name in the path for the image files to be saved in
        Uses a try except catch as it will throw an error if the folders already exists
        Adds User-Agent Headers to bypass 403 error
        Downloads the images into the folder of that recipe name'''

        self.makeImagesFolder()
        self.makeRecipeFolder()
        
        try:
            # Adds headers to resolve 403 Fobidden Error
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            downloadDirectory = "images/" + data.recipeDirectory + "/"
            fileType = '.jpg'
            fileName = downloadDirectory + recipeName + fileType
            image = urllib.request.urlretrieve(url, fileName)
        except:
            print("Error Downloading Images")           

    def makeImagesFolder() -> None:
        try:
            directory = "images"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Folder already exists: images")

    def makeRecipeFolder() -> None:
        try:
            data.recipeDirectory = data.recipeName.replace(".jpg", "").replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
            print("Recipe Name:" + data.recipeName)
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/images"
            path = os.path.join(parent_dir, data.recipeDirectory)
            os.mkdir(path)
            print("Directory '% s' created" % data.recipeDirectory)
        except:
            print("Folder already exists:", data.recipeDirectory)

    def makeImage(self, url) -> None:
        '''Retrieves the ID of each image using 'getRecipeDetails()
        Removes all unecissary elements from the ID string to create a file name
        Pass the file name to 'downloadImages() to create a file'''
        
        self.getRecipeDetails(self, url)
        
        for i in data.recipeDetails['Images']:

            for j in i:
                IDtoName = data.recipeDetails['ID'][0]
                IDtoName = IDtoName[0].replace("-", " ")
                IDtoName = IDtoName.title()

                for i in IDtoName:
                    if i.isdigit():
                        IDtoName = IDtoName.replace(i, "")

        s = str(data.count)
        data.recipeName = IDtoName + s + ".jpg"
        self.downloadImage(self, j, data.recipeName)
        data.count = data.count + 1                