import os # for testing directories
import requests # for testing website response
import unittest
import uuid # for testing the recipe unique identifyer
from scraper import scraper

class scraperTestCase(unittest.TestCase):

    recipe = 'harissa-spiced-beans-898-0.jpg'
    directory = 'C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline'

    @classmethod
    def setUpClass(cls): # Runs at the begining of the file
        pass

    @classmethod
    def tearDownClass(cls): # Runs at the end of the file
        pass

    def setUp(self): # Runs before every test
        self.bot1 = scraper() 
        self.friendlyID = 'harissa-spiced-beans-898'
        self.systemID = uuid.uuid4()
        self.dictionary = {"ID": []}
        self.number = str(3)
        self.recipeName = 'Harissa Spiced Beans'

        self.folderName = 'images'
        self.imagePath = os.path.join(self.directory, self.folderName)
        self.recipePath = os.path.join(self.directory, self.folderName)
        #self.handle = open("data.json", "r") # Dont forget to test the json file

    def tearDown(self): # Runs at the end of every test
        #print("tearDown\n")
        pass
    
    def test_dataClass(self):
        pass
    
    def test_decoratorClass(self):
        pass

    def test_run(self):
        pass

    def test_cycleRecipeLinks(self):
        pass

    def test_getURL(self):
        print("test_getURL")
        response = requests.get('https://www.pickuplimes.com/')

        if response.ok:
            print("Website Found")
            return response.text
        else:
            print("!Website Not Found!")
            return 'Bad Response'

        url = 'https://www.pickuplimes.com/'
        found = self.bot.driver.currentUrl
        self.assertEqual(url, found)


    def test_getTitle(self):
        pass

    def test_closeSession(self):
        pass

    def test_getSourceCode(self):
        pass

    def test_search(self):
        pass

    def test_searchbarTextAndClick(self):
        pass

    def test_findSearchbar(self):
        pass

    def test_home(self):
        pass

    def test_findRecipeList(self):
        pass

    def test_acceptCookies(self):
        pass

    def test_getRecipes(self):
        pass

    def test_getRecipeContainer(self):
        pass

    def test_makeRecipeList(self):
        pass

    def test_getPageURL(self):
        pass

    def test_getAllRecipePages(self):
        pass

    def test_getTotalPages(self):
        pass

    def test_getSearchList(self):
        pass

    def test_getUniqueID(self):
        pass

    def test_scrapeName(self):
        pass

    def test_scrapeTags(self):
        pass

    def test_scrapeDescription(self):
        pass

    def test_scrapeTotalTime(self):
        pass

    def test_scrapePrepTime(self):
        pass

    def test_scrapeCookTime(self):
        pass

    def test_scrapeAllergens(self):
        pass

    def test_scrapeAlternatives(self):
        pass

    def test_scrapeFreeFrom(self):
        pass

    def test_scrapeIngredients(self):
        pass

    def test_scrapeInstructions(self):
        pass

    def test_scrapeInstructions(self):
        pass

    def test_scrapeNotes(self):
        pass

    def test_scrapeStorage(self):
        pass

    def test_scrapeMainPhoto(self):
        pass

    def test_scrapeImages(self):
        pass

    def test_getRecipeDetails(self):
        pass

    def test_storeDetails(self):
        pass

    def test_jsonFile(self):
        pass

    def test_makeRaw_DataFolder(self):
        pass

    def jsonDump(self):
        pass

    # UNFINISHED
    def test_downloadImage(self):
        print('test_downloadImage')

        # Check directory path
        self.assertEqual(self.recipePath, 'C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline\images')

        # Check image name
        self.assertEqual(self.recipeName, 'Harissa Spiced Beans') 

        # Check image was downloaded

    # UNFINISHED
    def test_makeImagesFolder(self):
        print('test_makeImagesFolder')       

        # Check directory is correct
        self.assertEqual(self.imagePath, 'C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline\images') 

        # Check folder was created

    # PSEUDO
    def test_makeRecipeFolder(self):
        print('test_makeRecipeFolder')

        self.assertEqual(self.recipe.replace(".jpg", "").replace("0", ""), 'harissa-spiced-beans-898-')
        self.assertEqual(self.recipePath, 'C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline\images')
        self.assertEqual(os.path.join(self.recipePath, self.recipe), 'C:/Users/Millie/Documents/AiCore/AiCore/DataCollectionPipeline\images\harissa-spiced-beans-898-0.jpg')

    def test_makeImage(self):
        print("test_makeImage")

        self.dictionary['ID'].append(self.friendlyID)
        self.dictionary['ID'].append(self.systemID)

        # Check the dictionary contains the correct IDs
        self.assertEqual(self.dictionary['ID'][0], self.friendlyID)
        self.assertAlmostEqual(self.dictionary['ID'][1], self.systemID)

        # Check it removes all unnecessary bits from the string
        editedID = (self.dictionary['ID'][0])
        editedID = editedID.title()
        editedID = editedID.replace("-", " ")
        for i in editedID:
            if i.isdigit():
                editedID = editedID.replace(i , "")

        # Check the finished string is correct
        name = editedID + self.number + ".jpg"
        self.assertEqual(name, editedID + self.number + ".jpg") 

unittest.main(argv=['first-arg-is-ignored'], exit=False)

#if __name__ == "__main__":
#    test_scraper() 
#    print("Passed")