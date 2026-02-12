import allure
import os
import json
import urllib.parse
import pytest
from playwright.async_api import async_playwright

# BROWSER=chromium pytest        (Only Chromium – Local)
# BROWSER=firefox pytest         (Only Firefox – Local)
# BROWSER=webkit pytest          (Only WebKit – Local)
# pytest                         (All browsers – Local, default)

# EXECUTION_MODE=cloud pytest    (Cloud – LambdaTest)






def get_browsers():
    execution = os.getenv("EXECUTION_MODE", "local")

    if execution == "cloud":
        return ["cloud"]

    browser = os.getenv("BROWSER")
    if browser:
        return [browser]

    return ["chromium", "firefox", "webkit"]




@pytest.fixture(params=get_browsers())
async def page(request):
    execution = os.getenv("EXECUTION_MODE", "local")

    async with async_playwright() as p:

        # -------- CLOUD (LambdaTest) --------
        if execution == "cloud":
            username = os.getenv("LT_USERNAME")
            access_key = os.getenv("LT_ACCESS_KEY")

            assert username, "LT_USERNAME is not set"
            assert access_key, "LT_ACCESS_KEY is not set"

            capabilities = {
                "browserName": "chrome",
                "browserVersion": "142",
                "lt:options": {
                    "platform": "Windows 11",
                    "build": "Playwright Python sample1",
                    "name": "amazon test - playwright",
                    "user": username,
                    "accessKey": access_key,
                    "network": True,
                    "video": True,
                    "console": True
                }
            }

            caps = urllib.parse.quote(json.dumps(capabilities))
            ws_endpoint = (
                f"wss://cdp.lambdatest.com/playwright?capabilities={caps}"
            )

            browser = await p.chromium.connect(ws_endpoint)
            context = await browser.new_context()  #like incognito
            page = await context.new_page()
            await page.goto("https://practicetestautomation.com/practice-test-login/")


        # -------- LOCAL --------
        else:
            browser = await getattr(p, request.param).launch(
                headless=False
            )
            context = await browser.new_context()

        page = await context.new_page()
        await page.goto("https://practicetestautomation.com/courses/")

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