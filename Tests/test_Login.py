import pytest

from Utility.Webutility import Webutility


from playwright.async_api import Page

from pages.DashboardPage import Dashboard
from pages.LoginPage import  Login


#@pytest.mark.smoke (to execute based on tags)
#@pytest.mark.order(2)  (to execute in order wise )
#@pytest.mark.skip() (to skip)
#@allure.step("validating amazon login with valid credentials") it will not support aync mode

#@pytest.mark.dependency(name=["TC1"])
async def test_valid_login_test(page:Page):
    obj1 = Login(page)
    await obj1.EnterUsername()
    await Webutility.attach_screenshot(page, step_name="enter username", message="able to enter username successfully")


    await obj1.Enterpassword()
    await Webutility.attach_screenshot(page, step_name="enter password", message="able to enter password successfully")

    await obj1.clickonlogin()
    await Webutility.attach_screenshot(page, step_name="click login", message="able to login")


    obj2=Dashboard(page)
    await obj2.verifyDashboardTitle()
    await Webutility.attach_screenshot(page, step_name="verify title", message="landed on Dashboard Page")

#@pytest.mark.dependency(depends="TC1")
async def test_invalid_login_test(page:Page):
    obj1 = Login(page)
    await obj1.EnterUsername()
    await Webutility.attach_screenshot(page, step_name="enter invalid username", message="able to enter invalid username successfully")

    await obj1.Entervalidpassword()
    await Webutility.attach_screenshot(page, step_name="enter invalid password", message="able to enter invalid password successfully")

    await obj1.clickonlogin()
    await Webutility.attach_screenshot(page, step_name="click login", message="able to login ")

    await obj1.verifyerrormessage()
    await Webutility.attach_screenshot(page, step_name="verify error", message="able to validate error message ")




