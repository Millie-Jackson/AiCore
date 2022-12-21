from scraper import scraper

bot = scraper()

if __name__ == "__main__":
    bot.intitialize('https://www.pickuplimes.com/', 'lemons', 3)
else:
    print("Error: Driver closed because of initialize")
    bot.close()