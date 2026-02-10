import allure
import os
import pytest
from playwright.async_api import async_playwright

#BROWSER=chromium pytest  (Only Chrome)
#BROWSER=firefox pytest  (Only Firefox)
#BROWSER=webkit pytest  (Only WebKit)
#pytest   (All browsers (default))



def get_browsers():
    browser = os.getenv("BROWSER")
    if browser:
        return [browser]
    return ["chromium", "firefox", "webkit"]

@pytest.fixture(params=get_browsers())
async def page(request):
    async with async_playwright() as p:
        browser =await getattr(p, request.param).launch(headless=False)
        context =await browser.new_context()
        page =await context.new_page()
        await page.goto("https://the-internet.herokuapp.com/")

        yield page

        await context.close()
        await browser.close()




# ---------- PYTEST HOOK  ----------
# store test result on the item (sync hook)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# async fixture runs after each test and can await screenshot
@pytest.fixture(autouse=True)
async def screenshot_on_finish(request, page):
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep is None:
        return

    status = "PASSED" if rep.passed else "FAILED"
    screenshot_bytes = await page.screenshot(full_page=True)

    allure.attach(
        screenshot_bytes,
        name=f"{request.node.name} - {status}",
        attachment_type=allure.attachment_type.PNG
    )