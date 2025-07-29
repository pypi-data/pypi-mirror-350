from robot.api.deco import keyword
from .web_keywords import WebKeywords
from .desktop_keywords import DesktopKeywords


def get_library_instance():
    return DeskWebLib()

class DeskWebLib:
    def __init__(self, browser="chrome", implicit_wait=5):
        self.web = WebKeywords(browser=browser, implicit_wait=implicit_wait)
        self.desktop = DesktopKeywords()



    @keyword
    def open_browser(self, url):
        print("called here")
        return self.web.open_browser(url)

    @keyword
    def go_to(self, url):
        return self.web.go_to(url)

    @keyword
    def click_element(self, locator):
        return self.web.click_element(locator)

    @keyword
    def input_text(self, locator, text):
        return self.web.input_text(locator, text)

    @keyword
    def get_text(self, locator):
        return self.web.get_text(locator)

    @keyword
    def maximize_browser_window(self):
        return self.web.maximize_browser_window()

    @keyword
    def element_should_contain(self, locator, expected):
        return self.web.element_should_contain(locator, expected)

    @keyword
    def wait_until_element_is_visible(self, locator, timeout=10):
        return self.web.wait_until_element_is_visible(locator, timeout)

    @keyword
    def capture_screenshot(self, filename="screenshot.png"):
        return self.web.capture_screenshot(filename)

    @keyword
    def close_browser(self):
        return self.web.close_browser()

    # Desktop (Sikuli-style) functions
    @keyword
    def image_based_mouseclick(self, picture, mousebutton, click,current_scale,target_scale,confidence=0.8):
        return self.desktop.image_based_mouseclick(picture, mousebutton, click,current_scale,target_scale, confidence)

    @keyword
    def check_log_entries(self, start_time, check_log, file_path):
        return self.desktop.check_log_entries(start_time, check_log, file_path)

    @keyword
    def clear_log_file(self, file_path):
        return self.desktop.clear_log_file(file_path)

    @keyword
    def launch_application(self,app_name, delay=1):
        return self.desktop.launch_application(app_name, delay)

    @keyword
    def send_text(self,text, interval=0.05):
        return self.desktop.send_text(text, interval)
