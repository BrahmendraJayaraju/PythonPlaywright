
import json
import re

from playwright.async_api import expect


class Webutility:

    def Get_datafrom_json(self,testdata_path,key):
        # read
        with open(testdata_path, "r", encoding="utf-8") as d:
            data = json.load(d)

        return data[key]

    #for click operations with different locator types
    async def click(self, page, locator_type, locator_value, index=None):
        locator_type = locator_type.lower()

        if locator_type == "text":
            element = page.get_by_text(locator_value)

        elif locator_type == "title":
            element = page.get_by_title(locator_value)

        elif locator_type == "role":
            element = page.get_by_role(locator_value)


        elif locator_type == "label":
            element = page.get_by_label(locator_value)

        elif locator_type == "alt_text":
            element = page.get_by_alt_text(locator_value)

        elif locator_type == "test_id":
            element = page.get_by_test_id(locator_value)

        elif locator_type == "placeholder":
            element = page.get_by_placeholder(locator_value)

        elif locator_type == "locator":  # css / xpath
            element = page.locator(locator_value)

        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")

        if index is not None:
            element = element.nth(index)

        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.click()

    #for text comparison with different locator types
    async def compare_text(
            self, page, locator_type, locator_value, expected_text, index=None
    ):
        locator_type = locator_type.lower()

        if locator_type == "text":
            element = page.get_by_text(locator_value)

        elif locator_type == "title":
            element = page.get_by_title(locator_value)

        elif locator_type == "role":
            element = page.get_by_role(
                locator_value["role"],
                name=locator_value.get("name")
            )

        elif locator_type == "label":
            element = page.get_by_label(locator_value)

        elif locator_type == "alt_text":
            element = page.get_by_alt_text(locator_value)

        elif locator_type == "test_id":
            element = page.get_by_test_id(locator_value)

        elif locator_type == "placeholder":
            element = page.get_by_placeholder(locator_value)

        elif locator_type == "locator":  # css / xpath
            element = page.locator(locator_value)

        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")

        if index is not None:
            element = element.nth(index)

        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        actual_text = await element.inner_text()

        assert actual_text == expected_text, (
            f"Text mismatch: expected '{expected_text}', got '{actual_text}'"
        )


    #to verify title of webpage
    async def assert_title(self, page, expected_title, timeout=5000):
        await expect(page).to_have_title(expected_title, timeout=timeout)

    #to verify url of webpage
    async def assert_url(self, page, expected_url, timeout=5000):
        await expect(page).to_have_url(expected_url, timeout=timeout)

    # to verify partial title of webpage
    async def assert_title_partial(self, page, expected_title, timeout=5000):
        await expect(page).to_have_title(re.compile(expected_title), timeout=timeout)

    # to verify partial url of webpage
    async def assert_url_partial(self, page, expected_url, timeout=5000):
        await expect(page).to_have_url(re.compile(expected_url), timeout=timeout)

    async def tocheck_element_visible(self, page, locator_type, locator_value, index=None, timeout=5000):
        locator_type = locator_type.lower()

        if locator_type == "text":
            element = page.get_by_text(locator_value)

        elif locator_type == "title":
            element = page.get_by_title(locator_value)

        elif locator_type == "role":

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

        await element.scroll_into_view_if_needed()
        await expect(element).to_be_visible(timeout=timeout)


    #clears and enters text
    async def clear_entertext(self, page, locator_type, locator_value, text_to_fill, index=None):
        locator_type = locator_type.lower()

        if locator_type == "text":
            element = page.get_by_text(locator_value)

        elif locator_type == "title":
            element = page.get_by_title(locator_value)

        elif locator_type == "role":

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

        await element.scroll_into_view_if_needed()
        await element.wait_for(state="visible")
        await element.fill(text_to_fill)