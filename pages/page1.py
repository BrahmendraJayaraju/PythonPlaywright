

from playwright.async_api import Page

from Utility.Webutility import Webutility




class page1:

    def __init__(self, page:Page):

        self.page=page
        self.locator_path="./Locators/sample1.json"
        self.webutil = Webutility()
        self.seleniumlink= self.webutil.Get_datafrom_json(self.locator_path,"elementselenium")

    async def clickseleniumlink(self):

        await self.webutil.click_by_locator(self.seleniumlink,self.page)