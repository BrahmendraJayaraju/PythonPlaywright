

from playwright.async_api import Page

from Utility.Webutility import Webutility




class page1:

    def __init__(self, page:Page):

        self.page=page
        self.webutil = Webutility()
        self.locator_path = "./Locators/sample1.json"
        self.datapath="./Dataset/sample1.json"

        self.sen=self.webutil.Get_datafrom_json(self.locator_path,"lin")

        self.element= self.webutil.Get_datafrom_json(self.locator_path,"element")

        self.name=self.webutil.Get_datafrom_json( self.datapath,"name")
        #self.url= self.webutil.Get_datafrom_json(self.datapath, "url")


    async def tovisiblecheck(self):

        await self.webutil.tocheck_element_visible(self.page,"locator" ,self.sen)



    async def clearentertext(self):
        await self.webutil.click(self.page, "locator", self.sen)
        await self.webutil.clear_entertext(self.page,"locator" ,self.element,self.name )


