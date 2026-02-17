from playwright.async_api import Page

from Utility.Webutility import Webutility




class Dashboard:

    def __init__(self, page:Page):
        self.page=page
        self.webutil = Webutility()
        self.locator_path = "./Locators/Dashboard_locator.json"
        self.data_path = "./Dataset/Login_data.json"
        self.data_path_dashboard = "./Dataset/Dashboard_data.json"

        self.avatar=self.webutil.Get_datafrom_json(self.locator_path,"avatar_xpath")
        self.logout = self.webutil.Get_datafrom_json(self.locator_path, "logout_xpath")
        self.dashboard=self.webutil.Get_datafrom_json(self.locator_path,"dashboardXpath")
        self.dashboardtext=self.webutil.Get_datafrom_json(self.data_path_dashboard,"dashboardtext")


    async def clickonAvatar(self):
        await self.webutil.clickwebelement( self.page,"locator",self.avatar)

    async def clickonlogout(self):
        await self.webutil.clickwebelement(self.page, "locator", self.logout)


    async def verifyDashboardTitle(self):
        await self.webutil.compare_text(self.page, "locator", self.dashboard,self.dashboardtext)


