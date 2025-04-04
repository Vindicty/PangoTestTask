import pytest
import allure

from appium.webdriver.extensions.android.activities import Activities

from automation_framework.config import APK_PATH
from automation_framework.utilities import ApiHelper, attach_html_table_to_pytest_html

from test_data import TEST_CITIES



class TestMobileWeatherAPP:

    @pytest.fixture(autouse=True)
    def setup_tests(self, appium_driver, config, test_logger, page_factory, db_helper):
        """Initialize API client before each test."""

        self.driver = appium_driver
        self.db_helper = db_helper

        self.home_page = page_factory('home_page')
        self.settings_page = page_factory('settings_page')

        self.api_key = config['API_KEY']
        self.api = ApiHelper(base_url=config['BASE_URL'], api_key=self.api_key)

        self.log = test_logger


        self.db_helper.ensure_column_exists("app_temp", "REAL")
        self.db_helper.ensure_column_exists("temp_diff", "REAL")

    @allure.title("Check weather temperature from app and compare with OpenWeather API for multiple cities")
    def test_weather_setup(self):
        """Verify that temperature shown in the mobile app matches the OpenWeather API for a given city."""

        with allure.step("1. Set temperature unit to Celsius in the app"):
            self.home_page.click(self.home_page.SETTINGS_BUTTON)
            self.settings_page.click(self.settings_page.CUSTOMIZE_UNITS)
            self.settings_page.set_temperature_measurement('°C')
            self.settings_page.return_to_home_screen()

        with allure.step("2. Get temperature from APP for all cities"):
            app_temp_data = self.home_page.get_city_temperature(list(TEST_CITIES.keys()))

        with allure.step("3. Get temperature from API for all cities"):
            api_temp_data = {
                city: self.api.get_current_weather(id=city_id).json()['main']['temp']
                for city, city_id in TEST_CITIES.items()
            }

        with allure.step("5. Insert API & App weather data into DB"):
            for city in api_temp_data:
                api_temp = round(api_temp_data[city])
                app_temp = app_temp_data[city]

                # calculate absolute difference between api and app temperature values
                temp_diff = abs(app_temp - api_temp)

                self.db_helper.insert_weather_data(
                    city,
                    api_temperature=api_temp,
                    app_temp=app_temp,
                    temp_diff=temp_diff
                )

        with allure.step('6. Extraact Cities where difference between API and APP data is greater than 0'):
            resp = self.db_helper.get_weather_records(
                fields=["city", "api_temperature", "app_temp", "temp_diff"],
                where_clause="temp_diff > ?",
                params=(0,)
            )

            if resp:
                attach_html_table_to_pytest_html(
                    rows=resp,
                    headers=["City", "API Temp", "App Temp", "Difference"],
                    title="Difference Found Between API and APP"
                )

                pytest.fail(f"{len(resp)} cities have temperature differences. See attached table.")






