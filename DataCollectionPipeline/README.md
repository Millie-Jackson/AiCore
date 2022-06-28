DESCRIPTION
A webscraper that runs off the recipe website 'Pick Up Limes'. The goal is scraping and comparing recipies with similar names from more than one site in order to create a 'master' copy of common recipes detailing essential and optional ingrediants rather than having multiple varients of the same recipe. This website was used for its user friendly simplicity and decent amount of data to crawl. The topic is also relivant and useful to the industry as cooking is a part of everyday life and specifically veganism has become popular recently. This model would be valuable for those in the industry looking to reduce the psychological concept of decision fatuigue which is a well established issue in marketing/advertising/retail, and also for individual use who want to simplyfy their cooking/lifestyle.

It would be ideal if the model could take in a list of ingrediants (and kitchen tools) available in an individuals home and make suggestions on what meals could be made using whats currently available. Profiles could than be used within a app using common profile, diatry and lifestyle options

WEBSITESdata.recipeName
pickuplimes.com 
    - author is a dietician and influencer
    - recipes are designed to be simple and maximise nutrition
avantguardevegan.com 
    - author is a chef and influencer
    - recipes are on the more 'advanced' and complicated side

The contents for both sites where chosen because they compliment each other, ranging from 'easy to advanced' and 'practical to one-off-events'. There are multiple recipes for the same dish for comparison.

TECHNOLOGY: 
Python:        
    -commonly used for web scraping and data crawling
Selenium:
    - it is a popular freeware automation tool, its also open source and has good documentaion.
    - it can also run multiple scripts on multiple urls at once which matched the end goal of scraping and comparing recipies with similar names from more than one site
Chrome Driver:
    - chrome is the dominant browser
Requests:       
    - chosen for its various options to access html elements and was found to have more prectical to use than BeautifulSoup. 
    - it can also be used on multiple sites at once
UUID:
    - used to generate a unique id for each recipe for system use
    - industry standard method
JSON:
    - easily readable by both human and computer
    - used in web-based applications for browser to server exchange
    - works like a python dictionary
    - Has a key and corrisponding value
VSCode:
    - an industry standard and great pairing for Python
GutHub:
    - industry standard and was used for its version control

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
    - finds cookie button and clicks it to remove (there is no iframe on this website), uses a try statement to catch exceptions incase there is no cookie button
    - creates a unique user friends ID based on the page url for catagorising and debugging
    - creates a UUID for each recipe
Scraping:
    - gets the url (when navigating to a specific page or storing recipe pages for later use)
    - finds the first page of recipes, returnes the url and modifies it in order to predict the next page url. Each url is then stored in a list which displays its size. Currently capped at 5 for performance reasons. It cant detect how many total pages there are on a site yet
    - retrieves text and image data froma recipe page using XPaths
    - writes all scrapped details to a JSON file (text and image links)
    - downloads images into recipe specific files
    - Extra: gets the websites source code
    - Extra: gets the title (to be used when navigating home)
    - Extra: counts how many recipes are on that page and displays the titles

![image](https://user-images.githubusercontent.com/100158073/165974032-499039e8-4c97-48a0-bed5-ba5bd6aca19e.png)

User Friendly ID
- Create a user friendly id by editing the recipe page url, removing the unnecessary characters with .repace and keeping the default id defined by the website 
- Used for debugging and catagorising
(Recipe name -> 3 diget identifier)

UUID
- Creates a system id using UUID, a 124 bit lable, use is standard in the industry

Scrapes Recipe Details
- Finds the element and downloads the text using .text
- Finds the image container and stores the link for each image in a list
- Stores each element in a dictionary. Most elements are single strings, the last element is a list of image links
- Uses error hadndling and wait functions for flexability

JSON File
- Creates a folder to store JSON files in
- Uses error handeling incase the file already exists
- Handels error 'TypeError: Object of type UUID is not JSON serializable' by encoding the UUID by changing the type of the UUID
- Writes the recipe details dictionary to a JSON files
- Handels error 'TypeError: Object of type WebElement is not JSON serializable' by converting the dictionary to a string

Downloads Images
- Create a directory with error handling incase the folder already exists
- Remove the numbers from the end of the user friendly ID and use it to create a recipe specific folder
- Solve 403 Forbidden Error by adding headers
- Create a filename using the recipe name and file type
