import time

from typing import Dict, List, Tuple, Union

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.webdriver import WebDriver


from .base_page import BasePage

class HomePage(BasePage):
    """ Page object representing the Home screen of the mobile weather application.

    Provides methods to interact with key elements of the home screen,
    such as retrieving temperature values and performing city search operations.

    @param WebDriver driver: The Appium driver instance used for interacting with elements.

    """

    TEMPERATURE_SCREEN = (AppiumBy.XPATH, '(//android.widget.TextView[contains(@text, "°")])[1]')
    SETTINGS_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Go to settings"]')
    SEARCH_FIELD_ICON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Search"]')
    SEARCH_INPUT = (AppiumBy.XPATH, '//android.widget.EditText[@text="Search"]')
    SEARCH_SUGGESTION = '(//android.widget.TextView[contains(@text, "%s")])[1]'


    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def get_displayed_temperature(self) -> int:
        """Returns the temperature displayed on the home screen as an integer value."""

        raw_temp = self.get_text(self.TEMPERATURE_SCREEN)
        return int(raw_temp.replace("°C", "").strip())

    def get_city_temperature(self, cities: Union[str, List[str]]) -> Dict[str, str]:
        """ Searches for one or more cities in the weather app and retrieves their temperature values.

        If a single city name is provided, it will be wrapped in a list. For each city, this method:
        - Opens the search field
        - Enters the city name
        - Confirms the search via keyboard
        - Selects the first suggestion
        - Waits for the temperature to appear
        - Stores the result in a dictionary

        @param string/list cities: A single city name or a list of city names to search
        @return: Dictionary mapping each city name to its temperature string from the app
        """
        if isinstance(cities, str):
            cities = [cities]

        city_temp_data = {}

        for city in cities:
            self.click(self.SEARCH_FIELD_ICON)
            self.click(self.SEARCH_INPUT)
            self.enter_text(self.SEARCH_INPUT, city)

            self.driver.press_keycode(AndroidKey.ENTER)

            suggestion_locator = (AppiumBy.XPATH, self.SEARCH_SUGGESTION % city)
            self.click(suggestion_locator)

            self.find_element(self.TEMPERATURE_SCREEN)
            city_temp_data[city] = self.get_displayed_temperature()

        return city_temp_data





