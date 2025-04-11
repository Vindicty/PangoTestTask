import logging
import os
import subprocess
from configparser import ConfigParser
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from pytest_html import extras

from automation_framework.config import CONFIG_FILE, DB_PATH, APK_PATH, TEST_REPORTS_PATH
from automation_framework.pages import HomePage, WeatherSettingsPage
from automation_framework.utilities import DatabaseHelper, logger



def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="STAGE", help="Environment to run tests against: STAGE / PREPROD / PROD"
    )


@pytest.fixture(scope="function")
def appium_driver(request):
    """Initializes Appium driver using UiAutomator2Options with set_capability."""

    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", "emulator-5554")
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("app", str(APK_PATH))


    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def page_factory(appium_driver):
    """Session-scoped fixture that provides a factory for creating and caching page objects.

    This fixture generates page object instances based on a provided string name.
    Each page object is instantiated only once per session and stored in a cache,
    allowing efficient reuse across multiple tests.

    @param appium_driver: The Appium driver instance provided by the appium_driver fixture.
    @return: A function get_page(page_name: str) that returns a cached instance of the requested page object.

    @raises ValueError: If an unknown page_name is passed to the factory.

    Example:
        home_page = page_factory('home_page')
    """

    page_objects = {}

    def get_page(page_name):
        page_instances = {
            'home_page': HomePage,
            'settings_page': WeatherSettingsPage
        }

        if page_name not in page_objects:
            if page_name not in page_instances:
                raise ValueError(f"Unknown page: {page_name}")
            page_objects[page_name] = page_instances[page_name](appium_driver)


        return page_objects[page_name]

    return get_page

@pytest.fixture(scope='session')
def config(request):
    """Loads the configuration file and returns a ConfigParser object.  Used to access settings from config.ini."""

    env = request.config.getoption("--env")

    parser = ConfigParser()
    parser.read(CONFIG_FILE)

    return parser[env]


@pytest.fixture(scope="session")
def db_path(config):
    """Returns the full path to the database using base dir and file name from config."""

    db_name = config["DB_NAME"]
    return DB_PATH / db_name


@pytest.fixture(scope="session", autouse=True)
def test_logger():
    """ Provides the global logging instance to tests. """

    yield logger


@pytest.fixture(scope="class")
def db_helper():
    """Provides a DatabaseHelper instance for test class scope. Opens a database connection before tests and ensures
        it is closed after all class tests complete.
    """

    db = DatabaseHelper()
    yield db
    db.conn.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo) -> Generator[None, None, TestReport]:
    """Pytest hook to modify the test report after each test phase (setup, call, teardown).

    This hook checks if a custom HTML table was previously attached via the
    `attach_html_table_to_pytest_html` function and appends it as an extra section
    to the pytest-html report. The table is only attached during the "call" phase of the test.

    @param _pytest.nodes.Item item: The test item object containing info about the test function.
    @param _pytest.runner.CallInfo call: The test call object that includes the phase being executed.
    """

    outcome = yield
    report = outcome.get_result()

    if call.when == "call" and hasattr(pytest, "extra_html_table"):
        extra = getattr(report, "extra", [])
        extra.append(extras.html(pytest.extra_html_table))
        report.extra = extra