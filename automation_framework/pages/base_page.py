from typing import Literal, Tuple, Union

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement


# Type alias for locator tuples (strategy, value), used across multiple page objects.
# Declared at module level to promote reuse and improve readability in type hints.
Locator = Tuple[AppiumBy, str]

class BasePage:
    """ase class for all page objects in the mobile automation framework.

    Provides shared functionality for interacting with elements,
    such as waiting for presence, visibility, or clickability of elements.

    @param appium.webdriver.webdriver driver: The Appium WebDriver instance used to interact with the app.
    @param integer timeout: Default wait timeout for element interactions (in seconds).
    """
    def __init__(self, driver, timeout=35):
        self.driver = driver
        self.timeout = timeout

    def find_element(self,
                     locator: Locator,
                     wait_for: Literal["presence", "visible", "clickable"] = "presence") -> WebElement:
        """
        Waits for the specified condition and returns the found element.

        @param tuple locator: Container that contains type of locaor and locator ite (By, value)
        @param string wait_for: Type of wait: 'presence', 'visible', or 'clickable'
        @return: WebElement
        """
        wait = WebDriverWait(self.driver, self.timeout)

        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
        }

        if wait_for not in conditions:
            raise ValueError("Invalid wait_for value. Choose from: 'presence', 'visible', 'clickable'.")

        return wait.until(conditions[wait_for](locator))

    def click(self, element: Union[WebElement, Locator]) -> None:
        """Clicks on the given element or locator.

        If a locator tuple (By, value) is provided, waits until the element is present,
        finds it, and then clicks it. If a WebElement is provided, clicks it directly.

        @param tuple/Webelement: A locator tuple (By, value) or an already located WebElement.
        @raises TimeoutException: If the element is not found within the timeout period.
        """

        if not isinstance(element, WebElement):
            element = self.find_element(element, wait_for="clickable")

        element.click()

    def get_text(self, element: Union[WebElement, Locator]) -> str:
        """Extracts text from found element

        if type of element is not Webelement, waits untill element is present, find it and gets text.
        If a WebElement is provided, clicks it directly.

        @param tuple/Webelement element: A locator tuple (By, value) or an already located WebElement.
        @raises TimeoutException: If the element is not found within the timeout period.
        """

        if type(element) is not WebElement:
            element = self.find_element(element)

        return element.text

    def enter_text(self, element: Union[WebElement, Locator], text: str) -> None:
        """ Clears the input field and enters the given text.

        @param tuple/WebElement element: WebElement or locator tuple (By, value)
        @param text: str, text to input
        """
        if type(element) is not WebElement:
            element = self.find_element(element)

        element.clear()
        element.send_keys(text)

