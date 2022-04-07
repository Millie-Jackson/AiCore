#import numpy as np

from scraper import scraper
import time

bot = scraper()

scraper.getURL('https://www.pickuplimes.com/')
scraper.getTitle()
#scraper.getSourceCode()
scraper.acceptCookies()
#scraper.search("lemon")
#time.sleep(3)
scraper.home()
scraper.findRecipeList()
scraper.getRecipes()
#time.sleep(3)
scraper.closeSession()