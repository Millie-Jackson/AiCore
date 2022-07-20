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

from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

from decorators import exceptionHandling # used for genral exception handling
from decorators import scrapeHandling # used for scraping specific exception handling
from decorators import folderAlreadyExists # used for folder creation

#driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')

class data:

    articles = [] # Used to make a list of recipes
    button = None # Used to interact with various button elements
    container = None # Used to store various container elements
    count = 0 # Used in the creation of image filenames
    currentURL = "" # Used to store various urls 
    pages = [] # Used to append a list with pages links
    recipeDetails = {} # Used to store all the scraped recipe details
    recipeDirectory = "" # Used to create modified folder names
    recipeLinks = [] # Used to store recipe links
    recipeName = "" # Stores the recipe name
    searchbar = None # Used to interact with search bar
    source = "" # Used to get page source code
    tag = None # Used to store various tag elements
    title = "" # Used to get the title
    totalPages = [] # Stores a list of pages

    # Scraped Information
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
    def intitialize(self, url, searchTerm, delay):
        global_ids = scraper.__getUniqueID(scraper, 'https://www.pickuplimes.com/recipe/spicy-garlic-wok-noodles-213')
    
        self.__getURL(url) # Have to start somewhere
        self.__run()
        self.__closeSession() # Have to end somewhere

    def __run(self):
        #self.__acceptCookies()
        data.currentURL = self.__findRecipeList()
        self.__getAllRecipePages(data.currentURL)
        self.__getRecipes(data.currentURL)
        self.__cycleRecipeLinks()
        self.__closeSession()   

    def __cycleRecipeLinks(self):
        for i in data.recipeLinks:
            data.currentURL = i
            self.__makeImage(data.currentURL)

    def __getURL(self, url):
        '''Navigates to a website using a url passed as a perameter.'''
        driver.get(url) 

    def getTitle():
        '''Fetches the title and prints it to screen.'''
        data.title = driver.title

    def closeSession():
        '''Closes the driver'''
        driver.quit()

    def getSourceCode():
        '''Fetches source code for the page.'''
        data.source = driver.page_source

    @exceptionHandling
    def __search(self, searchTerm):
        '''Finds search bar, types in the search term which it takes as a perameter and clicks to navigate to the next page.'''
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-searchbar-btn')))
        button.click()

        self.findSearchbar(self, searchTerm)

    def searchbarTextAndClick(searchTerm):
        try:
            data.searchbar.send_keys(searchTerm)
            data.searchbar.send_keys(Keys.RETURN) # Return = Enter
        except:
            print("Exception: No search term input")
    
    @exceptionHandling
    def __findSearchbar(self, searchTerm):

        data.searchbar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "sb")))
        self.__searchbarTextAndClick(searchTerm)

    @exceptionHandling
    def __home():
        '''Finds the title and clicks it.'''
        title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-image')))
        title.click()

    @exceptionHandling
    def __findRecipeList(self):
        '''Finds the recipe tab and clicks it.'''
        data.button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recipes')))
        data.button.click()

    @exceptionHandling
    def __acceptCookies():
        '''Finds the accept cookies button and clicks it.'''
        data.button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]')))
        data.button.click()
    
    def __getRecipes(self, url):
        '''Finds the recipe container and puts all the recipes in a list.'''

        self.__getRecipeContainer()
        self.__makeRecipeList()

    @exceptionHandling
    def __getRecipeContainer(self):
        data.container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='index-item-container']/div/div[2]/ul"))) 

    def __makeRecipeList(self):
        data.articles = data.container.find_elements(By.TAG_NAME, 'li')

        for i in data.articles:
            data.tag = i.find_element(By.TAG_NAME, 'a')
            data.recipeLinks.append(data.tag.get_attribute('href'))

    def __getPageURL():
        '''Returns the current page url.'''
        data.currentURL =  driver.current_url

    def __getAllRecipePages(self, url):
        '''Navigates to each recipe page by modifying the current url and stores them in a list.'''

        self.__getTotalPages()
        self.__getSearchList()

    @exceptionHandling
    def __getTotalPages(self):
         #totalPages = driver.find_element(By.CLASS_NAME, 'page-text') #actual
        data.totalPages = [1, 2, 3] #temp to shorten runtime

    def __getSearchList(self):
        for i in data.totalPages:
            data.currentURL = driver.current_url
            url_change = "?page=" + str(i)
            next_page = data.currentURL + url_change
            data.pages.append(next_page)

    def __getUniqueID(self, url):
        '''Creates a uuid for each recipe taking a url as a perameter'''
        
        page_ID = url
        just_ID = page_ID.replace(str("https://www.pickuplimes.com/recipe/"), "")

        ids = (just_ID, uuid.uuid4())

    @scrapeHandling(data.name)
    def __scrapeName(self):

        data.name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/h1'))).text

    @scrapeHandling(data.recipeTags)
    def __scrapeTags(self):

        data.recipeTags = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header-info-col"]/div/header/a[1]/div/p'))).text

    @scrapeHandling(data.description)
    def __scrapeDescription(self):

        data.description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-info-col"]/div/header/span'))).text

    @scrapeHandling(data.timeTotal)
    def __scrapeTotalTime(self):
        
        data.timeTotal = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[2]'))).text  

    @scrapeHandling(data.timePrep)
    def __scrapePrepTime(self):

        data.timePrep = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[3]'))).text

    @scrapeHandling(data.timeCook)
    def __scrapeCookTime(self):
        
        data.timeCook = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-info-container"]/div[4]'))).text

    @scrapeHandling(data.allergens)
    def __scrapeAllergens(self):

        data.allergens = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[1]/div'))).text 

    @scrapeHandling(data.alternatives)
    def __scrapeAlternatives(self):
        
        data.alternatives = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[2]/div'))).text

    @scrapeHandling(data.freeFrom)
    def __scrapeFreeFrom(self):
        
        data.freeFrom = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="allergen-info-container"]/div[3]/div'))).text 

    @scrapeHandling(data.ingredients)
    def __scrapeIngredients(self):
        
        data.ingredients = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[2]'))).text

    @scrapeHandling(data.instructions)
    def __scrapeInstructions(self):
        
        data.instructions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ol'))).text

    @scrapeHandling(data.notes)
    def __scrapeNotes(self):
        
        data.notes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[1]/li'))).text

    @scrapeHandling(data.storage)
    def __scrapeStorage(self):
        
        data.storage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ingredient-direction-container"]/div/div[4]/section/ul[2]/li'))).text

    @scrapeHandling(data.mainPhoto)
    def __scrapeMainPhoto(self):
        
        data.mainPhoto = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-image-container"]/img')))


    @exceptionHandling
    def __scrapeImages(self):
        imageContainer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipe-video"]/div[2]'))) # Find the container
        imageList = imageContainer.find_elements(By.XPATH, 'img') # Find the children

        for i in imageList:
            link = i.get_attribute('src')
            data.imageLinks.append(link)

    @exceptionHandling
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
        self.__getURL(url)

        self.__scrapeName()  
        self.__scrapeTags()
        self.__scrapeDescription()
        self.__scrapeTotalTime()
        self.__scrapePrepTime()
        self.__scrapeCookTime()
        self.__scrapeAllergens()
        self.__scrapeAlternatives()
        self.__scrapeFreeFrom()
        self.__scrapeIngredients()
        self.__scrapeInstructions()
        self.__scrapeNotes()
        self.__scrapeStorage()
        self.__scrapeMainPhoto()
        self.__scrapeImages()

        self.__storeDetails(url)
        self.jsonFile()

    def __storeDetails(self, url):
        data.recipeDetails = {'ID': [], 'Name': [], 'Photo': [],'Tags': [], 'Description': [], 'Total Time': [], 'Prep Time': [], 'Cook Time': [], 'Allergens': [], 'Swaps': [], 'Free From': [], 'Ingredients': [], 'Directions': [], 'Notes': [], 'Storage': [], 'Images': []}
        data.recipeDetails['ID'].append(self.__getUniqueID(url))
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
        '''This function creates a folder for the json file to be stored in
        
        This function creates a folder called 'raw_data' in the path for the 
        json file to be saved in. Uses a try except catch as it will throw an 
        error if the folder already exists.

        Args:

        Returns:
        
        '''

        self.__makeRaw_DataFolder()

        # Deals with TypeError: Object of type UUID is not JSON serializable by encoding the UUID
        JSONEncoder_olddefault = JSONEncoder.default
        def JSONEncoder_newdefault(self, o):
            if isinstance(o, UUID): return str(o)
            return JSONEncoder_olddefault(self, o)
        JSONEncoder.default = JSONEncoder_newdefault

        self.jsonDump()
        
    @folderAlreadyExists("raw_data")
    def __makeRaw_DataFolder():      
        data.dataDirectory = "raw_data"
        parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
        path = os.path.join(parent_dir, data.dataDirectory)
        os.mkdir(path)
        print("Directory '% s' created" % data.dataDirectory)
    
    def jsonDump(self) -> None:
        '''This function writes the dictionary data to a json file
        
        This function stores data by writing the 'recipe_details' dictionary to a JSON file called 'data.json' in the folder just created
        The dicrionary is converted to a string using str() to deal with 'TypeError: Object of type WebElement is not JSON serializable
        
        Args:
        
        Returns:
        
        '''
        
        with open(os.path.join('raw_data', 'data.json'), 'w') as json_file:
            json.dump(str(data.recipeDetails), json_file)

    def downloadImage(self, url, recipeName):
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

    @folderAlreadyExists("Images")
    def __makeImagesFolder(self):
        
        data.imageDirectory = "images"
        parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline"
        path = os.path.join(parent_dir, data.imageDirectory)
        os.mkdir(path)
        print("Directory '% s' created" % data.imageDirectory)

    @folderAlreadyExists("Recipe")
    def __makeRecipeFolder(self):

        data.recipeDirectory = data.recipeName.replace(".jpg", "").replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
        parent_dir = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/images"
        path = os.path.join(parent_dir, data.recipeDirectory)
        os.mkdir(path)
        print("Directory '% s' created" % data.recipeDirectory)

    def __makeImage(self, url):
        '''Retrieves the ID of each image using 'getRecipeDetails()
        Removes all unecissary elements from the ID string to create a file name
        Pass the file name to 'downloadImages() to create a file'''
        
        self.getRecipeDetails(url)
        
        for i in data.recipeDetails['Images']:
            for j in i:
                IDtoName = str(data.recipeDetails['ID']).split()
                IDtoName1 = str(IDtoName[0]).replace("(", "")
                IDtoName2 = str(IDtoName1).replace("[", "")
                IDtoName3 = str(IDtoName2).replace(",", "")
                IDtoName4 = str(IDtoName3).replace("'", "")

                data.recipeName = IDtoName4 + "-" + str(data.count) + ".jpg"
                self.__downloadImage(self, j, data.recipeName)
                data.count = data.count + 1                