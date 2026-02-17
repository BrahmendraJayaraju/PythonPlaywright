from playwright.async_api import Page
from Utility.Webutility import Webutility



class page1:

    def __init__(self, page:Page):

        self.page=page
        self.page2=None
        self.webutil = Webutility()
        self.locator_path = "./Locators/login_locator.json"
        self.datapath="./Dataset/Login_data.json"
        self.locator1= self.webutil.Get_datafrom_json(self.locator_path,"element1")







    async def method1(self):
        pass






















