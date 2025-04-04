from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from .base_page import BasePage


class WeatherSettingsPage(BasePage):
    """Page object for the Settings screen in the weather application.

    Provides functionality to change temperature units (°C/°F)
    and navigate back to the home screen.

    @param WebDriver driver: The Appium driver used to interact with the mobile app.
    """

    CUSTOMIZE_UNITS = (AppiumBy.XPATH, '//android.widget.TextView[@text="Customize units"]')
    TEMP_UNIT_TOGGLE  = '//android.view.ViewGroup[@content-desc="%s"]'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def set_temperature_measurement(self, unit: str) -> None:
        """ Sets the temperature unit (°C or °F) by clicking the corresponding toggle.

        @param unit: Unite type "°C" or "°F"
        """
        if unit not in ("°C", "°F"):
            raise ValueError("Unit must be '°C' or '°F'")

        self.click((AppiumBy.XPATH, self.TEMP_UNIT_TOGGLE % unit))


