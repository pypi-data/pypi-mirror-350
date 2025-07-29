from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebKeywords:
    def __init__(self, browser="chrome", implicit_wait=5):
        self.driver = None
        self.browser = browser
        self.implicit_wait = implicit_wait

    def open_browser(self, url: str):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

        self.driver.implicitly_wait(self.implicit_wait)
        self.driver.get(url)

    def go_to(self, url: str):
        self.driver.get(url)

    def click_element(self, locator: str):
        if locator.startswith("xpath="):
            by = By.XPATH
            locator_value = locator.replace("xpath=", "", 1)
        elif locator.startswith("css="):
            by = By.CSS_SELECTOR
            locator_value = locator.replace("css=", "", 1)
        elif locator.startswith("id="):
            by = By.ID
            locator_value = locator.replace("id=", "", 1)
        else:
            raise ValueError(f"Unsupported locator format: {locator}")

        self.driver.find_element(by, locator_value).click()

    def input_text(self, locator: str, text: str):
        if locator.startswith("xpath="):
            by = By.XPATH
            locator_value = locator.replace("xpath=", "", 1)
        elif locator.startswith("css="):
            by = By.CSS_SELECTOR
            locator_value = locator.replace("css=", "", 1)
        elif locator.startswith("id="):
            by = By.ID
            locator_value = locator.replace("id=", "", 1)
        else:
            raise ValueError(f"Unsupported locator format: {locator}")

        element = self.driver.find_element(by, locator_value)
        element.clear()
        element.send_keys(text)

    def parse_locator(self,locator: str):
        if locator.startswith("xpath="):
            return By.XPATH, locator[6:]
        elif locator.startswith("css="):
            return By.CSS_SELECTOR, locator[4:]
        elif locator.startswith("id="):
            return By.ID, locator[3:]
        else:
            raise ValueError(f"Unsupported locator: {locator}")

    def get_text(self, locator: str) -> str:
        by, value = self.parse_locator(locator)
        return self.driver.find_element(by, value).text

    def element_should_contain(self, locator: str, expected: str):
        text = self.get_text(locator)
        assert expected in text, f"Expected '{expected}' to be in '{text}'"

    def maximize_browser_window(self):
        self.driver.maximize_window()

    def wait_until_element_is_visible(self, locator: str, timeout: int = 10):
        by, value = self.parse_locator(locator)
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    def capture_screenshot(self, filename="screenshot.png"):
        self.driver.save_screenshot(filename)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
