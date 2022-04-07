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
scraper.quit()

#bot = scraper.Scraper('https://www.metasrc.com/5v5')
#bot.accept_cookies('Cookie Accept Path', 'iFrame Path') # Site doenst have cookies
#bot.click_search_bar('Search Bar Path')
#bot.write_in_search_bar('Hello', 'Path')
#time.sleep(2)

print("End")


