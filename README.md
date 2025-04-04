# 📱 Mobile Weather App Test Framework

This is a UI + API test automation framework for a mobile weather application.  
It uses **Python**, **Pytest**, **Appium**, **pytest-html**, and **SQLite**.

The framework is designed for clarity, maintainability, and extendability.  
It follows clean architecture principles and good testing practices.

---

## 🚀 Features

### ✅ UI Tests with Appium
- Launch the mobile weather app on an emulator or real device
- Set temperature units via the settings page
- Retrieve temperature values from the app
- Compare the values with OpenWeather API
- Log results and fail the test if there's a mismatch

### ✅ API + DB Validation
- Fetch data from the OpenWeather API
- Save it into a local SQLite database
- Validate the consistency of stored values

### ✅ Parametrized Testing
I use `pytest.mark.parametrize` to run tests for multiple cities.  
This enables:
- Independent test results for each city
- Easier debugging
- Clean and scalable structure

### ✅ HTML Reporting (`pytest-html`)
- A styled HTML report is generated after every test run
- The report includes:
  - Summary and test results
  - Attached HTML table showing cities with temperature mismatches (API vs APP)
- Output is saved to:  
  `automation_framework/tests/logs/report.html`

### ✅ Logging
- Global logger (`logger.py`) captures key actions:
  - App installation
  - API calls
  - Database writes
- Logs are saved to:  
  `automation_framework/tests/logs/test_run.log`

### ✅ SQLite Support
- Data is stored in `data.db`
- Auto-creation of tables on the first run
- Easily query mismatches by city

---

## 🧭 Project Structure

### `automation_framework/config/`  
Stores framework configuration:
- `config.ini` – User-editable config file
- `paths.py` – Constants for directories and file paths

### `automation_framework/db/`  
- `data.db` – SQLite database with weather data

### `automation_framework/mobile_apps/`  
- `OpenWeather_1.1.7_APKPure.apk` – Test APK file

### `automation_framework/pages/`  
Page Object Model:
- `base_page.py` – Base class for all page objects
- `home_page.py` – Home screen interactions
- `settings_page.py` – Settings screen interactions

### `automation_framework/tests/`  
- `logs/`
  - `report.html` – HTML test report with table of mismatches
- `test_data/`
  - `test_mobile_weather_app.py` – UI test with validation against API
  - `test_openweather_api.py` – API + DB validation
  - `cities.py` – List of cities for test parametrization
- `utilities/`
  - `api_helpers.py` – HTTP calls to OpenWeather API
  - `db_helpers.py` – Database helpers
  - `logger.py` – Logger setup
  - `reporting.py` – HTML table generation for reports

### Root Files
- `conftest.py` – Pytest fixtures and hooks (HTML table injection)
- `pytest.ini` – Configures `pytest-html` output path
- `requirements.txt` – Dependencies
- `README.md` – This documentation

---

## 🛠 Setup Instructions

### ✅ Prerequisites
- Python 3.9+
- Appium server running
- Android emulator or real device
- Android SDK with emulator properly configured

### 🔽 Install dependencies
```bash
pip install -r requirements.txt
```

### ▶ Run Tests
```bash
pytest
```

By default, the test report will be saved to:  
`automation_framework/tests/logs/report.html`

---

## 🧪 Example Report

The report includes:
- Environment and platform info
- Per-test status (Passed, Failed)
- Embedded HTML table showing cities with mismatches (if any)

You can view the report by opening the HTML file directly in your browser.

---

## ✅ Status

This framework is under active development and serves as a clean reference project  
for combining mobile UI, API testing, and reporting.

Contributions and improvements are welcome!
