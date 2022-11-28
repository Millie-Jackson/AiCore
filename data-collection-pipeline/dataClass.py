class data:
    '''
    This class contains all the attributes of the scraper

    Attributes:
            articles : (list) 
                Used to make a list of recipes
            button : (none) 
                Used to interact with various button elements
            container : (none)
                Used to store various container elements
            currentURL : (str)
                Used to store various urls 
            pages : (list)
                Used to append a list with pages links
            recipeLinks : (list) 
                Used to store recipe links
            searchbar : (none)
                Used to interact with search bar
            source : (str)
                Used to get page source code
            tag : (none)
                Used to store various tag elements
            title : (str)
                Used to get the title
            totalPages : (list)
                Stores a list of pages
            count : (int)
                Used in the creation of image filenames
            parentDirectory : (str)
                Project directory
            dataDirectory : (str)
                Used to create folder
            imageDirectory : (str)
                Used to create folder 
            recipeDirectory : (str)
                Used to create modified folder names
            imageFileName : (str)
                Used to create image files
            jsonFileName : (str)
                Used to create json files
            recipeDetails : (dict)
                Used to store all the scraped recipe details
            imageScrapeLimiter : (int)
                Used to limit the amount of times an image is scraped
            allergens : (str)
                Used to store scraped allergens
            alternatives : (str)
                Used to store scraped alternatives
            description : (str)
                Used to store the scraped description of the recipe
            freeFrom : (str)
                Used to store the scraped free from information
            imageLinks : (list)
                Used to scrape all of a recipes image links
            ingredients : (str)
                Used to store the scraped ingredients
            instructions : (str)
                Used to store scraped instructions
            mainPhoto : (none)
                Used to store main photo link
            name : (str)
                Used to store scraped recipe name
            notes : (str)
                Used to store scraped recipe notes
            recipeTags : (str)
                Used to store scraped recipe tags
            storage : (str)
                Used to store scraped storage instructions
            timeCook : (str)
                Used to store scraped cook time
            timePrep : (str)
                Used to store scraped recipe  prep time 
            timeTotal : (str)
                Used to store scraped total time it takes to make the recipe
            bucketName : (str)
                Used to access the S3 bucket
        

    Functions:

    '''

    articles = [] # Used to make a list of recipes
    button = None # Used to interact with various button elements
    container = None # Used to store various container elements
    currentURL = "" # Used to store various urls 
    pages = [] # Used to append a list with pages links
    recipeLinks = [] # Used to store recipe links
    searchbar = None # Used to interact with search bar
    source = "" # Used to get page source code
    tag = None # Used to store various tag elements
    title = "" # Used to get the title
    totalPages = [] # Stores a list of pages

    # File Management
    count = 0 # Used in the creation of image filenames
    parentDirectory = "C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline/" # Project directory
    dataDirectory = "raw_data" # Used to create folder
    imageDirectory = "" # Used to create folder 
    recipeDirectory = "" # Used to create modified folder names
    imageFileName = "" # Used to create image files
    jsonFileName = "" # Used to create json files

    # Scraped Information
    recipeDetails = {} # Used to store all the scraped recipe details
    imageScrapeLimiter = 0 # Used to limit the amount of times an image is scraped

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
    bucketName = 'data-collection-pipeline-bucket' # Used to access the S3 bucket