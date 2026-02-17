
from Utility.Webutility import Webutility


from playwright.async_api import Page

from pages.page1 import page1


#@pytest.mark.smoke
#@pytest.mark.dependency(depends=["TC1"])
#@pytest.mark.order(2)
#@pytest.mark.skip()

#@allure.step("validating amazon login with valid credentials") it will not support aync mode

async def test_tc01(page:Page):
    obj1 = page1(page)

    # Step 1
    await obj1.method1()
    await Webutility.attach_screenshot(page, step_name="Login Step", message="Opened login page successfully")

    # Step 2
    #await obj1.method2()
    #await Webutility.attach_screenshot(page, step_name="After Actions", message="Completed actions successfully")

#@pytest.mark.dependency(name="TC1")
#async def test_tc02(page:Page):
   # obj1 = page1(page)
    #await obj1.clearentertext()
