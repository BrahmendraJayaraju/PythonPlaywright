import pytest
from playwright.async_api import Page

from pages.page1 import page1


#@pytest.mark.smoke
#@pytest.mark.dependency(depends=["TC1"])
#@pytest.mark.order(2)
#@pytest.mark.skip()
async def test_tc01(page:Page):
    obj1 = page1(page)
    await obj1.method1()
    await obj1.method2()

#@pytest.mark.dependency(name="TC1")
#async def test_tc02(page:Page):
   # obj1 = page1(page)
    #await obj1.clearentertext()
