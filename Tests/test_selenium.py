
from playwright.async_api import Page

from pages.page1 import page1



async def test_tc01(page:Page):
    obj1 = page1(page)
    await obj1.clickseleniumlink()

async def test_tc02(page:Page):
    obj1 = page1(page)
    await obj1.clickabtest()
    await obj1.veriftextinside()