import allure
import pytest

from automation_framework.utilities import ApiHelper

from test_data import TEST_CITIES


class TestWeatherAPI:

    @pytest.fixture(autouse=True)
    def setup_tests(self, config, db_path, test_logger, db_helper):
        """Initialize API client before each test."""

        self.api_key = config['API_KEY']
        self.api = ApiHelper(base_url=config['BASE_URL'], api_key=self.api_key)
        self.db_helper = db_helper
        self.log = test_logger

        self.db_helper.ensure_column_exists(column_name='average_temperature', column_type='REAL')


    @allure.title("Check that weather API and DB data are consistent for city: {city}")
    @pytest.mark.parametrize('city', TEST_CITIES.keys())
    def test_temp_and_feels_like_by_city_name(self, city):
        """Check that weather API returns 200 for a valid city."""

        with allure.step("1. Request weather from API by city name"):
            response = self.api.get_current_weather(q=city)
            assert response.status_code == 200, f"Couldn't get weather for {city}"

            temp_data = response.json()['main']
            api_temperature, api_feels_like = temp_data['temp'], temp_data['feels_like']


        with allure.step("2. Insert weather data into DB"):
            self.db_helper.insert_weather_data(city=city, api_temperature=api_temperature, feels_like=api_feels_like)

        with allure.step("3. Get weather data from DB and compare"):
            db_temperature, db_feels_like = self.db_helper.get_weather_data(
                city, fields=["api_temperature", "feels_like"]
            )

            assert db_temperature == api_temperature, (
                f'Temp mismatch for {city}: DB={db_temperature}, API={api_temperature}'
            )

            assert db_feels_like == api_feels_like, (
                f'Feels_like mismatch for {city}: DB={db_feels_like}, API={api_feels_like}'
            )

    @pytest.mark.parametrize('city_name, city_id', TEST_CITIES.items())
    @allure.title("Check average temperature in DB for city: {city_name}")
    def test_avg_temp_by_city_id(self, city_name, city_id):
        with allure.step("1. Request weather from API by city id"):
            response = self.api.get_current_weather(id=city_id)
            assert response.status_code == 200, f"Couldn't get weather for {city_id}"

        with allure.step("3. Extract and aggregate API temperature data"):
            temp_data = response.json()['main']
            api_temperature, api_feels_like = temp_data['temp'], temp_data['feels_like']
            api_avg_temperature = round((temp_data['temp_min'] + temp_data['temp_max'])/2, 2)

        with allure.step("4. Insert weather data into DB"):
            self.db_helper.insert_weather_data(
                city=city_name,
                api_temperature=api_temperature,
                feels_like=api_feels_like,
                average_temperature=api_avg_temperature
            )

        with allure.step("5. Validate average_temperature in DB matches API"):
            db_data = self.db_helper.get_weather_data(city=city_name, fields=["average_temperature"])
            db_avg_temp = db_data[0]
            assert db_avg_temp == api_avg_temperature, (
                f"{city_name}: mismatch avg temp! DB={db_avg_temp}, API={api_avg_temperature}"
            )

    @allure.title("Report hottest city from DB")
    def test_report_max_avg_temp(self):
        city, max_avg_temp = self.db_helper.get_aggregated_value("average_temperature", "MAX")
        self.log.info(f"Hottest city: {city} with {max_avg_temp}°C")

        assert city is not None and  max_avg_temp is not None





