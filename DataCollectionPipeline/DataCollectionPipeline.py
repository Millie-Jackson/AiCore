#import numpy as np

from scraper import scraper
import time

bot = scraper()

if __name__ == "__main__":
    bot.intitialize('https://www.pickuplimes.com/', 'lemons', 5)
else:
    print("Error: Driver closed because of initialize")
    bot.close()