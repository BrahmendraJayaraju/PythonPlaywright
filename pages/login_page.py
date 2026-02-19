from playwright.async_api import Page
from utils.Webutility import Webutility



class Login:

    def __init__(self, page:Page):

        self.page=page
        self.page2=None
        self.webutil = Webutility()
        self.locator_path = "./locators/login_locator.json"
        self.datapath="./test_data/Login_data.json"

        self.locator_path_dashboard = "./locators/Dashboard_locator.json"
        self.datapath_dashboard = "./test_data/Dashboard_data.json"

        self.username= self.webutil.Get_datafrom_json(self.locator_path,"username_xpath")
        self.password = self.webutil.Get_datafrom_json(self.locator_path, "password_xpath")
        self.login= self.webutil.Get_datafrom_json(self.locator_path, "login_btn_xpath")
        self.usernmamedata = self.webutil.Get_datafrom_json(self.datapath, "username")
        self.pwddata= self.webutil.Get_datafrom_json(self.datapath, "password")
        self.pwddatainvalid=self.webutil.Get_datafrom_json(self.datapath, "Invalidpassword")
        self.loginheadertext= self.webutil.Get_datafrom_json(self.locator_path, "loginheader")
        self.text=self.webutil.Get_datafrom_json(self.datapath, "loginheadertext")
        self.dashboard=self.webutil.Get_datafrom_json( self.locator_path_dashboard,"dashboardXpath")
        self.dashboardtext=self.webutil.Get_datafrom_json( self.datapath_dashboard, "dashboardtext")
        self.login= self.webutil.Get_datafrom_json(self.locator_path, "loginheader")
        self.logintext=self.webutil.Get_datafrom_json(self.datapath, "loginheadertext")





    async def EnterUsername(self):
        await self.webutil.clear_entertext(self.page,"locator",self.username,self.usernmamedata)

    async def Enterpassword(self):
        await self.webutil.clear_entertext(self.page,"locator",self.password,self.pwddata)

    async def clickonlogin(self):


        await self.webutil.clickwebelement(self.page, "role", "Login")








    async def Entervalidpassword(self):
        await self.webutil.enter_by_type(self.page,"locator",self.password,self.pwddatainvalid)



    async def verifyerrormessage(self):



        await self.webutil.compare_text(self.page,"locator",self.loginheadertext,self.text)


    async def verifyDashboardTitle(self):
        await self.webutil.compare_text(self.page, "locator", self.dashboard, self.dashboardtext)

    async def verifyloginpage(self):
        await self.webutil.compare_text(self.page, "locator", self.login,self.logintext )




























