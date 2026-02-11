
import json

class Webutility:

    def Get_datafrom_json(self,testdata_path,key):
        # read
        with open(testdata_path, "r", encoding="utf-8") as d:
            data = json.load(d)

        return data[key]

    async def click_by_locator(self, locator, page):
        await page.locator(locator).scroll_into_view_if_needed()
        await page.locator(locator).wait_for(state="visible")
        await page.locator(locator).click()


    async def gettextandverify(self,locator,expectedtext,page):
        await page.locator(locator).wait_for(state="visible")
        actualtext=await page.locator(locator).inner_text()
        assert actualtext==expectedtext, f"Text mismatch: expected '{expectedtext}', got '{actualtext}'"






