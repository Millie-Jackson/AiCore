import functools # used to maintain introspection on decorators
import requests
import urllib
import boto3 # used to access AWS resources
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

import decorators
from decorators import exceptionHandling # used for genral exception handling
from decorators import scrapeHandling # used for scraping specific exception handling
from decorators import folderAlreadyExists # used for folder creation

#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


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

    # Cloud Management
    bucket = 'data-collection-pipeline-bucket'

class scraper:
    def intitialize(self, url, searchTerm):
        global_ids = scraper.getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
    
        self.getURL(url) # Have to start somewhere
        self.run()
        self.closeSession() # Have to end somewhere

    def run(self) -> None:
        '''
        This function calls all the necissary functions in order.

        The order of function calls is for the class to navigate 
        through the website and scrape the text and images.

        Args:

        Returns:

        '''
        
        #self.acceptCookies()
        data.currentURL = self.findRecipeList()
        self.getAllRecipePages(data.currentURL)
        self.getRecipes(data.currentURL)
        self.cycleRecipeLinks()
        self.closeSession()   

    def cycleRecipeLinks(self) -> None:
        '''
        This function iterates though the list of recipe urls, passing each url to the makeImage() function.

        Args:

        Returns:

        '''

        for i in data.recipeLinks:
            data.currentURL = i
            self.makeImage(data.currentURL)

    def getURL(self, url) -> None:
        '''
        Navigates to a website using a url passed as a perameter.
        
        Args:
            url (str): The target website
        
        Returns:

        '''

        driver.get(url) 

    def getTitle(self) -> None:
        '''
        Fetches the title.
        
        Args:
        
        Returns:
        
        '''

        data.title = driver.title

    def closeSession(self) -> None:
        '''
        Closes the driver
        
        Args:
        
        Returns:
        
        '''

        driver.quit()

    def getSourceCode(self) -> None:
        '''
        Fetches the current pages source code.
        
        Args:

        Returns:

        '''

        data.source = driver.page_source

    @decorators.exceptionHandling
    def search(self, searchTerm) -> None:
        '''
        Finds search bar and clicks it ready for input.
        
        Args:
            searchTerm (str): The word passed to the findSearchBar() fucntion that types into the search box
        
        Returns:

        '''

        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-searchbar-btn')))
        button.click()

        self.findSearchbar(self, searchTerm)

    def searchbarTextAndClick(self, searchTerm) -> None:
        '''
        This function types the searchTerm into the searchbar and presses enter which then navigates to the search results page.

        Args:
            searchTerm (str): The word to type into the search box

        Returns:
        
        '''

        try:
            data.searchbar.send_keys(searchTerm)
            data.searchbar.send_keys(Keys.RETURN) # Return = Enter
        except:
            print("Exception: No search term input")
    
    @decorators.exceptionHandling
    def findSearchbar(self, searchTerm) -> None:
        '''
        This function finds the searchbar and calls the searchbarTextAndClick() function with the searchTerm parameter.

        Args: 
            searchTerm (str): The word passed to the searchbarTextAndClick() fucntion that types into the search box

        Returns:
        
        '''

        data.searchbar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "sb")))
        self.searchbarTextAndClick(searchTerm)

    @decorators.exceptionHandling
    def home(self) -> None:
        '''
        Finds the title and clicks it.
        
        Args:
        
        Returns:
        
        '''

        title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-image')))
        title.click()

    @decorators.exceptionHandling
    def findRecipeList(self) -> None:
        '''
        Finds the recipe tab and clicks it.
        
        Args:
        
        Returns:
        
        '''

        data.button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
        data.button.click()

    @decorators.exceptionHandling
    def acceptCookies(self) -> None:
        '''
        Finds the accept cookies button and clicks it.
        
        Args:
        
        Returns:
        
        '''

        data.button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]')))
        data.button.click()
    
    def getRecipes(self, url) -> None:
        '''
        Calls the functions to find the recipe container and puts all the recipes in a list.
        
        Args:
            url (str): The target website that contains all the recipe search results
        
        Returns:
        
        '''

        self.getRecipeContainer()
        self.makeRecipeList()

    @decorators.exceptionHandling
    def getRecipeContainer(self) -> None:
        '''
        This function finds the recipe container

        Args:

        Returns:

        '''

        data.container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='index-item-container']/div/div[2]/ul"))) 

    def makeRecipeList(self) -> None:
        '''
        This function finds the individual recipe page link and stores it in a list

        This function finds an individual recipes link by identifying the container 
        with all the recipes, then loops through that contain to find the individual 
        recipes and takes the url for that recipe and stores it in a list.
        
        Args:

        Returns:

        '''

        data.articles = data.container.find_elements(By.TAG_NAME, 'li')

        for i in data.articles:
            data.tag = i.find_element(By.TAG_NAME, 'a')
            data.recipeLinks.append(data.tag.get_attribute('href'))

    def getPageURL() -> None:
        '''
        Returns the current page url.
        
        Args:

        Returns:

        '''

        data.currentURL =  driver.current_url

    def getAllRecipePages(self, url) -> None:
        '''
        Calls the functions to navigate to each recipe page by modifying the current url and stores them in a list.
        
        Args:
            url (str): The target website that contains all the recipe search results
        
        Returns:
        
        '''

        self.getTotalPages()
        self.getSearchList()

    @decorators.exceptionHandling
    def getTotalPages(self) -> None:
        '''
        This function counts the total number of page results.

        Args:

        Returns:
        
        '''

         #totalPages = driver.find_element(By.CLASS_NAME, 'page-text') #actual
        data.totalPages = [1, 2, 3] #temp to shorten runtime

    def getSearchList(self) -> None:
        '''
        This function retrieves the url of each search result by modifying the url.

        Args:

        Returns:

        '''
        for i in data.totalPages:
            data.currentURL = driver.current_url
            url_change = "?page=" + str(i)
            next_page = data.currentURL + url_change
            data.pages.append(next_page)

    def getUniqueID(self, url) -> None:
        '''
        This function creates a uuid for each recipe by modifying  a url as a perameter. 

        Args: 
            url (str): The recipe page url

        Returns:

        '''
        
        page_ID = url
        just_ID = page_ID.replace(str("https://www.pickuplimes.com/recipe/"), "")

        ids = (just_ID, uuid.uuid4())

    def scrapeName(self) -> None:
        '''
        This function scrapes the name of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''
        try:    
            data.name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/h1'))).text
        except NoSuchElementException:
            print("Exception: Name Not Found")
            data.name = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Name")
            data.name = "N/A" 

    def scrapeTags(self) -> None:
        '''
        This function scrapes the tags of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.recipeTags = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header-info-col"]/div/header/a[1]/div/p'))).text
        except NoSuchElementException:
            print("Exception: Tag Not Found")
            data.recipeTags = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Tag")
            data.recipeTags = "N/A"

    def scrapeDescription(self) -> None:
        '''
        This function scrapes the description of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/span'))).text
        except NoSuchElementException:
            print("Exception: Description Not Found")
            data.description = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Description")
            data.description = "N/A"

    def scrapeTotalTime(self) -> None:
        '''
        This function scrapes the total cook time of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''
       
        try:
            data.timeTotal = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[2]'))).text  
        except NoSuchElementException:
            print("Exception: Total-Time Not Found")
            data.timeTotal = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Total-Time")
            data.timeTotal = "N/A"

    def scrapePrepTime(self) -> None:
        '''
        This function scrapes the prep time of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.timePrep = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[3]'))).text
        except NoSuchElementException:
            print("Exception: Prep-Time Not Found")
            data.timePrep = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Prep-Time")
            data.timePrep = "N/A"

    def scrapeCookTime(self) -> None:
        '''
        This function scrapes the cook time of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''
        
        try:
            data.timeCook = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[4]'))).text
        except NoSuchElementException:
            print("Exception: Cook-Time Not Found")
            data.timeCook = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Cook-Time")
            data.timeCook = "N/A" 

    def scrapeAllergens(self) -> None:
        '''
        This function scrapes the allergens of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.allergens = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div'))).text 
        except NoSuchElementException:
            print("Exception: Allergens Not Found")
            data.allergens = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Allergens")
            data.allergens = "N/A"

    def scrapeAlternatives(self) -> None:
        '''
        This function scrapes the alternative ingrediants of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try: 
            data.alternatives = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div'))).text
        except NoSuchElementException:
            print("Exception: Swap Not Found")
            data.alternatives = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Swap")
            data.alternatives = "N/A"

    def scrapeFreeFrom(self) -> None:
        '''
        This function scrapes what the recipe is free from. Exception handling is done with a decorator

        Args:

        Returns:

        '''
        try:
            data.freeFrom = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div'))).text 
        except NoSuchElementException:
            print("Exception: Free-From Not Found")
            data.freeFrom = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Free-From")
            data.freeFrom = "N/A" 

    def scrapeIngredients(self) -> None:
        '''
        This function scrapes the recipe ingredients. Exception handling is done with a decorator

        Args:

        Returns:

        '''
        
        try:
            data.ingredients = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]'))).text
        except NoSuchElementException:
            print("Exception: Ingredients Not Found")
            data.ingredients = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Ingredients")
            data.ingredients = "N/A"

    def scrapeInstructions(self) -> None:
        '''
        This function scrapes the instructions for the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.instructions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol'))).text
        except NoSuchElementException:
            print("Exception: Directions Not Found")
            data.instructions = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Directions")
            data.instructions = "N/A"

    def scrapeNotes(self) -> None:
        '''
        This function scrapes the notes from the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.notes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li'))).text
        except NoSuchElementException:
            print("Exception: Notes Not Found")
            data.notes = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Notes")
            data.notes = "N/A"

    def scrapeStorage(self) -> None:
        '''
        This function scrapes the storage instructions of the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''

        try:
            data.storage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li'))).text
        except NoSuchElementException:
            print("Exception: Storage Not Found")
            data.storage = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Storage")
            data.storage = "N/A"

    def scrapeMainPhoto(self) -> None:
        '''
        This function scrapes the main image from the recipe. Exception handling is done with a decorator

        Args:

        Returns:

        '''
        try:
            data.mainPhoto = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-image-container"]/img')))
        except NoSuchElementException:
            print("Exception: Main Image Not Found")
            data.mainPhoto = "N/A"
        except TimeoutException:
            print("Exception: Timeout: Didnt Find Main Image")
            data.mainPhoto = "N/A"

    @exceptionHandling
    def scrapeImages(self) -> None:
        '''
        This function scrapes the other images from the recipe. Exception handling is done with a decorator

        This function finds the image container then puts its children into a list. A limit is set based on the number of images found for later use. Finally the list is 
        iterated to get each images url link to create a list of image links

        Args:

        Returns:

        '''
        
        imageContainer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-video"]/div[2]'))) # Find the container
        imageList = imageContainer.find_elements(By.XPATH, 'img') # Find the children
        data.imageScrapeLimiter = len(imageList)

        for i in imageList:
            link = i.get_attribute('src')
            data.imageLinks.append(link)

    @decorators.exceptionHandling
    def getRecipeDetails(self, url) -> None:
        '''
        This function calls the scrape functions

        This function navigates to a recipe page and calls all the scrape functions to collect 
        the data from the page. It the calls the function that stores all the data in a dictionary 
        and calls the function that writes that dictionary to a json file

        Args:
            url (str): The recipe page url
        
        Returns:

        '''
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

        self.storeDetails(url)
        self.jsonFile()

    def storeDetails(self, url) -> None:
        '''
        This function updates the data dictionarl with all the scraped information

        Args: 
            url (str): The recipe url to make a unique ID

        Returns:

        '''

        data.recipeDetails = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        data.recipeDetails['ID'].append(self.getUniqueID(url))
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
        '''
        This function creates a folder for the json file to be stored in
        
        This function creates a folder called 'raw_data' in the path for the 
        json file to be saved in. Uses a try except catch as it will throw an 
        error if the folder already exists.

        Args:

        Returns:
        
        '''

        self.makeRaw_DataFolder()

        '''Deals with TypeError: Object of type UUID is not JSON serializable by encoding the UUID'''
        JSONEncoder_olddefault = JSONEncoder.default
        def JSONEncoder_newdefault(self, o):
            if isinstance(o, UUID): return str(o)
            return JSONEncoder_olddefault(self, o)
        JSONEncoder.default = JSONEncoder_newdefault

        self.jsonDump()

    def makeRaw_DataFolder(self) -> None:
        '''
        This function creates a folder.
        
        This function creates a folder for the json files to be stored in
        Throws an exception if the folder already exists which is handeled 
        with a decorator.

        Args:

        Returns:

        '''
        try:
            directory = "raw_data"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Folder already exists: raw_data")
    
    def jsonDump(self) -> None:
        '''This function writes the dictionary data to a json file
        
        This function creates a name for the json file using the scraped recipe name and appending it with the file type
        It stores data by writing the 'recipe_details' dictionary to a JSON file called 'data.json' in the folder just created
        The dicrionary is converted to a string using str() to deal with 'TypeError: Object of type WebElement is not JSON serializable
        The function to upload the json to the bucket is then called
        
        Args:
        
        Returns:
        
        '''

        data.jsonFileName = data.name + '.json'
        path = os.path.join('raw_data', data.jsonFileName)
        dir = os.path.join('C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/', data.jsonFileName)

        with open(dir, 'w') as json_file:
            json.dump(str(data.recipeDetails), json_file, indent = 6)
        
        self.__bucketJson(path, data.jsonFileName)

    def downloadImage(self, url) -> None:
        '''
        This function creates a folder.
        
        This function calls the function that creates a folder called 'images' 
        Then calls the function that creates a folder named after the recipes name 
        Adds User-Agent Headers in a try/catch exeption handler to bypass 403 error
        Downloads the image into the folder of that recipe name
        Calls the function that uploads the image to the bucket
        
        Args:
        
        Returns:
        
        '''
        self.makeImagesFolder()
        self.makeRecipeFolder()

        try:
            # Adds headers to resolve 403 Fobidden Error
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            path = os.path.join(data.recipeDirectory, data.imageFileName + '.jpg')
            urllib.request.urlretrieve(url, path)
        except:
            print("Error Downloading Images")
        
        self.__bucketImage(path, data.imageFileName)          

    def makeImagesFolder(self) -> None:
        '''
        This function makes a folder.

        This function Makes a folder called images for the recipe images to be stored in.
        Uses a try except catch in a decorator as it will throw an error if the folders already exists.

        Args:

        Returns:

        '''
        try:
            directory = "images"
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
        except:
            print("Folder already exists: images")

    def makeRecipeFolder(self) -> None:
        '''
        This function makes a folder.

        This function Makes a folder named after the recipe for the images to be stored in.
        Uses a try except catch in a decorator as it will throw an error if the folders already exists.

        Args:

        Returns:

        '''
        try:
            data.recipeDirectory = data.recipeName.replace(".jpg", "").replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
            parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/images"
            path = os.path.join(parent_dir, data.recipeDirectory)
            os.mkdir(path)
            print("Directory '% s' created" % data.recipeDirectory)
        except:
            print("Folder already exists:", data.recipeDirectory)

    def makeImage(self, url) -> None:
        '''
        This function makes a file name for the image and downloads it.
        
        This function retrieves the ID of each image using 'getRecipeDetails().
        Removes all unecissary elements from the ID string to create a file name.
        Pass the file name to 'downloadImages() to create a file.

        Args:
            url (str): The recipe url to scrape information from

        Returns:

        '''

        self.getRecipeDetails(url)

        for i in data.recipeDetails['Images']:
            
            for j in i:
                data.imageFileName = data.name + " " + str(data.count) + ".jpg"
                self.downloadImage(j)

                if data.count < data.imageScrapeLimiter:
                    data.count = data.count + 1
                else:
                    data.count = 0      

    def __bucketImage(self, path, imageFileName) -> None:
        '''
        This function uploads the image to the bucket
        
        Args:
             path(str): The directory the image is stored in
             imageFileName(str): The string used to name the image 
        
        Returns:
        
        '''

        # Uploads files to bucket
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(path, data.bucket, imageFileName) # (file_name, bucket, object_name)

    def __bucketJson(self, path, jsonFileName) -> None:
        '''
        This function uploads the json to the bucket
        
        Args:
             path(str): The directory the json is stored
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        # Uploads files to bucket
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(path, data.bucket, jsonFileName) # (file_name, bucket, object_name)

    def __bucketDownloadJson(self, url, jsonFileName) -> None:
        '''
        This function downloads the json into the local directory
        
        Args:
             url(str): The url for the file stored in the bucket
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        response = requests.get(url, jsonFileName)
        path = os.path.join('raw_data', jsonFileName)
        with open(path, 'wb') as f:
            f.write(response.content)

    def __bucketDownloadImage(self, url, imageFileName) -> None:
        '''
        This function downloads the image into the local directory
        
        Args:
             url(str): The url for the file stored in the bucket
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        response = requests.get(url, imageFileName)
        path = os.path.join('raw_data', imageFileName)
        with open(path, 'wb') as f:
            f.write(response.content)