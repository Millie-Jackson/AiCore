#import numpy as np

import scraper
import time

bot = scraper()

bot.getURL('https://www.pickuplimes.com/')
bot.getTitle()
#bot.getSourceCode()
bot.search("lemon")
bot.quit()

#bot = scraper.Scraper('https://www.metasrc.com/5v5')
#bot.accept_cookies('Cookie Accept Path', 'iFrame Path') # Site doenst have cookies
#bot.click_search_bar('Search Bar Path')
#bot.write_in_search_bar('Hello', 'Path')
#time.sleep(2)

print("End")


