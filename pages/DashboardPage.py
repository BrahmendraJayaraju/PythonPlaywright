from playwright.async_api import Page

from Utility.Webutility import Webutility




class page2:

    def __init__(self, page:Page):
        self.page=page
        self.webutil = Webutility()
        self.locator_path = "./Locators/sample2.json"

        self.add=self.webutil.Get_datafrom_json(self.locator_path,"addremove")

    async def clickaddremove(self):
        await self.webutil.click( self.page,"locator",self.add)