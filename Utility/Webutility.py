import json
import re
from playwright.async_api import expect

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
                element = page.get_by_role(locator_value)
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
    async def click(self, page, locator_type, locator_value, index=None):
        element = self._get_locator(page, locator_type, locator_value, index)
        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
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
    async def enter_by_type(self, page, locator_type, locator_value, text_to_type, index=None, delay=50):
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



