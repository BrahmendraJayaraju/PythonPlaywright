

from playwright.async_api import Page

from Utility.Webutility import Webutility




class page1:

    def __init__(self, page:Page):

        self.page=page
        self.webutil = Webutility()
        self.locator_path = "./Locators/sample1.json"
        self.datapath="./Dataset/sample1.json"
        self.seleniumlink= self.webutil.Get_datafrom_json(self.locator_path,"elementselenium")
        self.abtest= self.webutil.Get_datafrom_json(self.locator_path,"abtest")
        self.abtext=self.webutil.Get_datafrom_json(self.locator_path,"abwords")
        self.data=self.webutil.Get_datafrom_json( self.datapath,"absentense")

    async def clickseleniumlink(self):

        await self.webutil.click_by_locator(self.seleniumlink,self.page)


    async def clickabtest(self):
        await self.webutil.click_by_locator(self.abtest,self.page)


    async def veriftextinside(self):
        await self.webutil.gettextandverify(self.abtext,self.data,self.page)