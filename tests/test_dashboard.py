from playwright.async_api import Page

from utils.Webutility import Webutility
from pages.dashboard_page import Dashboard
from pages.login_page import Login


async def test_verify_logout(page:Page):
    obj1 = Login(page)
    await obj1.EnterUsername()
    await Webutility.attach_screenshot(page, step_name="enter username", message="able to enter username successfully")

    await obj1.Enterpassword()
    await Webutility.attach_screenshot(page, step_name="enter password", message="able to enter password successfully")

    await obj1.clickonlogin()
    await Webutility.attach_screenshot(page, step_name="click login", message="able to login ")


    obj2 = Dashboard(page)
    await obj2.clickonAvatar()
    await Webutility.attach_screenshot(page, step_name="click on avatar", message="user was able to see dropdown")

    await obj2.clickonlogout()
    await Webutility.attach_screenshot(page, step_name="click on logout", message="user was able to clcik on logout")



    await obj1.verifyloginpage()
    await Webutility.attach_screenshot(page, step_name="verify login page", message="user was able to land on login page")


