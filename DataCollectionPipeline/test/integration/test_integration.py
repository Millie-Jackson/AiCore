from scraper import scraper

class scraperIntegrationTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls): # Runs at the begining of the file
        pass

    @classmethod
    def tearDownClass(cls): # Runs at the end of the file
        pass

    def setUp(self): # Runs before every test
        print("setUp\n")
        self.bot1 = scraper()

    def tearDown(self): # Runs at the end of every test
        print("tearDown\n")

    def test_run(self):
        # Test __acceptCookies()
            # self.acceptCookies()
        # Test data.currentURL 
            # data.currentURL = self.__findRecipeList(self)
        # Test findRecipieList()
            # data.currentURL = self.__findRecipeList(self)
        # Test getAllRecipies()
            # self.__getAllRecipePages(self, data.currentURL)
        # Test getRecipes()
            # self.__getRecipes(self, data.currentURL)
        # Test cycleRecipeLinks()
            # self.__cycleRecipeLinks(self)
        # Test closeSession()
            # self.closeSession(self)

        pass
