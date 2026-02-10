
from playwright.async_api import Page

from pages.page1 import page1


async def test_seleniumlink(page:Page):
    obj1 = page1(page)
    await obj1.clickseleniumlink()