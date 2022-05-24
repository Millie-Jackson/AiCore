#import numpy as np

from scraper import scraper
from decorators import noSuchElementException
#import scraper
import time

bot = scraper()

if __name__ == "__main__":
    bot.intitialize('https://www.pickuplimes.com/', 'lemons')
else:
    print("Error: Driver closed because of initialize")
    bot.close()