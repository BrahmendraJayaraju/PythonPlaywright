from playwright.async_api import Page
from Utility.Webutility import Webutility
class page1:

    def __init__(self, page:Page):

        self.page=page
        self.page2=None
        self.webutil = Webutility()
        self.locator_path = "./Locators/locator1.json"
        self.datapath="./Dataset/data1.json"
        self.locator1= self.webutil.Get_datafrom_json(self.locator_path,"element1")
        self.locator2 = self.webutil.Get_datafrom_json(self.locator_path, "element2")
        self.locator3= self.webutil.Get_datafrom_json(self.locator_path, "element3")
        self.locator4 = self.webutil.Get_datafrom_json(self.locator_path, "element4")
        self.data1=self.webutil.Get_datafrom_json( self.datapath,"name")
        self.data2 = self.webutil.Get_datafrom_json(self.datapath, "pwd")
        self.locator5=self.webutil.Get_datafrom_json(self.locator_path, "element5")

    async def method1(self):

        await self.webutil.click(self.page, "locator", self.locator4)
        a=await self.webutil.switch_to_tab(self.page, "locator", self.locator5)
        self.page2=a

    async def  method2(self):
        await self.webutil.tocheck_element_visible(self.page2, "locator", self.locator1)
        a=await self.webutil.get_element_text(self.page2, "locator", self.locator1)
        print(a)
        await self.webutil.bring_page_to_front(self.page)

        await self.webutil.scroll_to_element(self.page, "locator", self.locator2)
        await self.webutil.close_page(self.page2)


















