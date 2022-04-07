#import numpy as np

from scraper import scraper
import time

bot = scraper()

bot.getURL('https://www.pickuplimes.com/')
bot.getTitle()
bot.acceptCookies()
bot.getAllRecipePages()
#scraper.getSourceCode()
#scraper.search("lemon")
#time.sleep(3)
#scraper.home()
#scraper.findRecipeList()
#scraper.getRecipes()
#scraper.getPageURL()
#time.sleep(3)
bot.closeSession()