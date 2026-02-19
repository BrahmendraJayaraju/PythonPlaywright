import json
import os
import re

import aiomysql
import asyncpg
from PIL import Image, ImageChops
import allure
from playwright.async_api import expect, Page


import asyncio

from playwright.async_api import Page

class Webutility:

    def Get_datafrom_json(self, testdata_path, key):
        with open(testdata_path, "r", encoding="utf-8") as d:
            data = json.load(d)
        return data[key]

    # Helper method to resolve a locator
    def _get_locator(self, page, locator_type, locator_value, index=None):
        locator_type = locator_type.lower()

        if locator_type == "text":
            element = page.get_by_text(locator_value)
        elif locator_type == "title":
            element = page.get_by_title(locator_value)
        elif locator_type == "role":
            if isinstance(locator_value, dict):
                role = locator_value.get("role")
                kwargs = {k: v for k, v in locator_value.items() if k != "role"}
                element = page.get_by_role(role, **kwargs)
            else:
                element = page.get_by_role("button", name=locator_value)
        elif locator_type == "label":
            element = page.get_by_label(locator_value)
        elif locator_type == "alt_text":
            element = page.get_by_alt_text(locator_value)
        elif locator_type == "test_id":
            element = page.get_by_test_id(locator_value)
        elif locator_type == "placeholder":
            element = page.get_by_placeholder(locator_value)
        elif locator_type == "locator":  # CSS / XPath
            element = page.locator(locator_value)
        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")

        if index is not None:
            element = element.nth(index)
        return element

    # Click an element
    async def clickwebelement(self, page:Page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.is_enabled()
        await element.click()

    # Compare text
    async def compare_text(self, page, locator_type, locator_value, expected_text, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        actual_text = await element.inner_text()
        assert actual_text == expected_text, f"Text mismatch: expected '{expected_text}', got '{actual_text}'"

    # Clear and enter text
    async def clear_entertext(self, page, locator_type, locator_value, text_to_fill, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.fill(text_to_fill)

    # Type text with delay
    async def enter_by_type(self, page, locator_type, locator_value, text_to_type, index=None, delay=5):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.type(text_to_type, delay=delay)

    # Clear input
    async def clear_text(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.clear()

    # Check element visibility
    async def tocheck_element_visible(self, page, locator_type, locator_value, index=None, timeout=5000):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await expect(element).to_be_visible(timeout=timeout)

    # Click radio button
    async def click_radio(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.click()

    # Check checkbox
    async def check_checkbox(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.check()

    # Uncheck checkbox
    async def uncheck_checkbox(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.uncheck()

    # Select dropdown option
    async def select_dropdown_option(self, page, locator_type, locator_value, option, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.select_option(option)

    # For scrolling to a specific element
    async def scroll_to_element(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()

    # Assert title/url helpers
    async def assert_title(self, page, expected_title, timeout=5000):
        await expect(page).to_have_title(expected_title, timeout=timeout)

    async def assert_url(self, page, expected_url, timeout=5000):
        await expect(page).to_have_url(expected_url, timeout=timeout)

    async def assert_title_partial(self, page, expected_title, timeout=5000):
        await expect(page).to_have_title(re.compile(expected_title), timeout=timeout)

    async def assert_url_partial(self, page, expected_url, timeout=5000):
        await expect(page).to_have_url(re.compile(expected_url), timeout=timeout)

    # To refresh the page
    async def refresh_page(self, page):
        await page.reload()

    # Go back to the previous page
    async def go_back(self, page):
        await page.go_back()

    # Go forward to the next page
    async def go_forward(self, page):
        await page.go_forward()

    # Wait for page to reach a specific load state
    #state="networkidle"
    async def wait_for_load_state(self, page, state="load", timeout=30000):

        await page.wait_for_load_state(state=state, timeout=timeout)

    # Generic wait_for function
    #state="visible" Wait until element is visible
    #state="hidden"  Wait until element is hidden
    #state="attached" Wait until element is attached to DOM
    async def wait_for(self, page, locator_type, locator_value, state="visible", index=None, timeout=5000):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state=state, timeout=timeout)

    # Get current page URL
    def get_current_url(self, page):

        return page.url

    # Get full page HTML
    async def get_page_content(self, page):
        return await page.content()

    # Get text of a specific element
    async def get_element_text(self, page, locator_type, locator_value, index=None):

        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        return await element.inner_text()

    #get address of new tab
    async def switch_to_tab(self, page, locator_type, locator_value, index=None):
        async with page.expect_popup() as new_page_info:
            await self.click(page, locator_type, locator_value, index)

        new_page = await new_page_info.value
        await new_page.wait_for_load_state()
        return new_page


    #to switch back to parent tab

    async def bring_page_to_front(self, page):
        await page.bring_to_front()


   #to close particular tab
    async def close_page(self, page):
        await page.close()

    #if you want to atatch screenshot after each step
    @staticmethod
    async def attach_screenshot(page: Page, step_name: str, message: str):
        # Attach text
        allure.attach(message, name=f"{step_name} - Text", attachment_type=allure.attachment_type.TEXT)
        # Attach screenshot
        screenshot = await page.screenshot(full_page=True)
        allure.attach(screenshot, name=f"{step_name} - Screenshot", attachment_type=allure.attachment_type.PNG)

    #keyboard actions  using mac , for windows some keys differs
    # to press single key like tab , enter
    async def press_key(self, page, key: str):
        await page.keyboard.press(key)

    #enter the text , macos
    async def type_text(self, page, text: str, delay: int = 50):
        await page.keyboard.type(text, delay=delay)


   #control+c and control+v like this actions , macos
    async def shortcut(self, page: Page, *keys: str):
        # Press all keys down
        for key in keys:
            await page.keyboard.down(key)
        # Release all keys in reverse order
        for key in reversed(keys):
            await page.keyboard.up(key)

    # to press key and hold it for some time , macos
    async def press_and_hold(self, page: Page, key: str, duration: float = 1):
        await page.keyboard.down(key)
        await page.wait_for_timeout(duration * 1000)
        await page.keyboard.up(key)

    #to clear using backspace macos
    async def clear_input(self, page: Page, selector: str):
        await page.locator(selector).click()
        await page.keyboard.press("Meta+A")
        await page.keyboard.press("Backspace")

    #to drag and drop
    async def drag_and_drop(self, page, source_locator_type, source_locator_value, target_locator_type,
                            target_locator_value, source_index=None, target_index=None):
        source = self._get_locator(page, source_locator_type, source_locator_value, source_index)
        target = self._get_locator(page, target_locator_type, target_locator_value, target_index)
        await source.scroll_into_view_if_needed()
        await target.scroll_into_view_if_needed()
        await source.drag_to(target)

    # Vertical scroll by a specific amount
    async def scroll_vertical(self, page: Page, pixels: int = 500, delay_ms: int = 3000):
        await page.wait_for_timeout(delay_ms)
        await page.mouse.wheel(0, pixels)

    # Horizontal scroll by a specific amount
    async def scroll_horizontal(self, page: Page, pixels: int = 500, delay_ms: int = 3000):
        await page.wait_for_timeout(delay_ms)
        await page.mouse.wheel(pixels, 0)

    # Scroll both horizontally and vertically
    async def scroll_both(self, page: Page, horizontal_pixels: int = 500, vertical_pixels: int = 500,
                          delay_ms: int = 3000):
        await page.wait_for_timeout(delay_ms)
        await page.mouse.wheel(horizontal_pixels, vertical_pixels)

    # Left click (default)
    async def left_click(self, page: Page, locator_type: str, locator_value: str, index: int = None,
                         delay_ms: int = 3000):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(delay_ms)
        await element.click()

    # Right click
    async def right_click(self, page: Page, locator_type: str, locator_value: str, index: int = None,
                          delay_ms: int = 3000):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(delay_ms)
        await element.click(button="right")

    # Double click
    async def double_click(self, page: Page, locator_type: str, locator_value: str, index: int = None,
                           delay_ms: int = 3000):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(delay_ms)
        await element.dblclick()


    #click on ok  in alert
    async def accept_alert(self, page: Page):
        async def handle_dialog(dialog):
            await dialog.accept()

        page.once("dialog", handle_dialog)


    #click on cancel  in alert
    async def dismiss_alert(self, page: Page):
        async def handle_dialog(dialog):
            await dialog.dismiss()

        page.once("dialog", handle_dialog)

    #send text in alert
    async def accept_prompt_with_text(self, page: Page, text: str):
        async def handle_prompt(dialog):
            await dialog.accept(text)

        page.once("dialog", handle_prompt)

    #get text in alert
    # Trigger the alert while waiting for it
    async def get_alert_text(self, page: Page, click_locator: str) -> str:
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async def handle_dialog(dialog):
            future.set_result(dialog.message)
            await dialog.accept()

        page.once("dialog", handle_dialog)
        await page.locator(click_locator).click()
        return await future



   #file upload
    async def upload_file(self, page: Page, locator_type: str, locator_value: str, file_path: str, index: int = None):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.set_input_files(file_path)
        return element

    #file download and attach in allure report
    async def download_file( self,page: Page,locator_type: str,locator_value: str,download_dir: str = None, index: int = None) :
        if download_dir is None:
            download_dir = os.path.join(os.getcwd(), "Downloads")
        os.makedirs(download_dir, exist_ok=True)
        element = self._get_locator(page, locator_type, locator_value, index)
        async with page.expect_download() as download_info:
            await element.click()
        download = await download_info.value
        file_path = os.path.join(download_dir, download.suggested_filename)
        await download.save_as(file_path)
        with open(file_path, "rb") as f:
            allure.attach(
                f.read(),
                name=download.suggested_filename,
                attachment_type=allure.attachment_type.TEXT
            )
        assert os.path.exists(file_path), f"File not found: {file_path}"
        return file_path




    # to compare two images
    async def compareimages(self, page: Page, image1: str, image2: str):
        await asyncio.to_thread(self._compare_images_sync, image1, image2)

    def _compare_images_sync(self, image1: str, image2: str):
        image1 = Image.open(image1).convert("RGB")
        image2 = Image.open(image2).convert("RGB")

        assert image1.size == image2.size, "Images have different sizes"

        diff = ImageChops.difference(image1, image2)
        assert diff.getbbox() is None, "Images are different"


    #to switch to specific frame

    async def  switchtoframe(self,page:Page,locator_type, locator_value, index=None):

          element = self._get_locator(page, locator_type, locator_value, index)
          return page.frame_locator(element )

   #select either future date or previous date or current date
    #only if not inside the frame use this
    async def select_date(
            self,
            page: Page,
            datepicker_locator_type: str,
            datepicker_locator_value: str,
            target_day: int,
            target_month: str,
            target_year: int,
            month_locator_type: str,
            month_locator_value: str,
            year_locator_type: str,
            year_locator_value: str,
            prev_button_locator_type: str,
            prev_button_locator_value: str,
            next_button_locator_type: str,
            next_button_locator_value: str,
            day_locator_type: str,
            day_locator_template: str,
            index: int = None
    ):

        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]


        # Get the datepicker container
        element=self._get_locator(page, datepicker_locator_type, datepicker_locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.click()

        while True:
            current_month = (
                await self._get_locator( page,month_locator_type, month_locator_value).text_content()).strip()
            current_year = (
                await self._get_locator( page,year_locator_type, year_locator_value).text_content()).strip()

            print(f"Current: {current_month} {current_year}")

            # If target reached, click the date
            if current_month == target_month and int(current_year) == target_year:
                day_locator_value = day_locator_template.format(day=target_day)
                await self._get_locator(page,day_locator_type, day_locator_value).click()
                break

            # Determine direction
            current_month_index = months.index(current_month)
            target_month_index = months.index(target_month)

            if int(current_year) > target_year or (
                    int(current_year) == target_year and current_month_index > target_month_index
            ):
                await self._get_locator(page, prev_button_locator_type, prev_button_locator_value).click()
            else:
                await self._get_locator(page,next_button_locator_type, next_button_locator_value).click()



    async def execute_db_query_async(
            self,
            db_type,
            host,
            user,
            password,
            database,
            port,
            query
    ):
        if db_type == "mysql":
            conn = await aiomysql.connect(
                host=host,
                user=user,
                password=password,
                db=database,
                port=port
            )

            async with conn.cursor() as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()

            conn.close()
            return result

        elif db_type == "postgres":
            conn = await asyncpg.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )

            result = await conn.fetch(query)
            await conn.close()

            # Convert asyncpg Record → tuple (to match MySQL output)
            return [tuple(row) for row in result]

        else:
            raise ValueError("Unsupported database type")




