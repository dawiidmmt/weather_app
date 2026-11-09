# Weather App

A desktop weather application built with **Python** and **PyQt5**. Type a city name and get the current weather, fetched live from the [OpenWeatherMap](https://openweathermap.org/) API.

## Features

- Current temperature, weather description and emoji icon
- Extra details: feels-like temperature, humidity and wind speed
- Background colour that changes with the temperature
- Search by pressing **Enter** or clicking the button
- Clear error messages for an empty field, an unknown city, a wrong API key, timeouts and connection problems
- Results in metric units, with descriptions in Polish

## Tech stack

- Python 3
- PyQt5 (GUI)
- requests (HTTP)
- OpenWeatherMap Current Weather API

## How to run

1. Clone the repository:
   ```bash
   git clone https://github.com/dawiidmmt/weather-app.git
   cd weather-app
   ```
2. Install the dependencies:
   ```bash
   pip install PyQt5 requests
   ```
3. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
4. Create a file called `config.py` in the project folder:
   ```python
   API_KEY = "your_api_key_here"
   ```
   `config.py` is listed in `.gitignore`, so your key never ends up on GitHub.
5. Run the app:
   ```bash
   python3 weather_app.py
   ```

## What I learned

- Calling a REST API with `requests` and reading the JSON response
- Handling errors properly: `raise_for_status()`, HTTP status codes with `match`/`case`, and the right order of `except` blocks
- Building a GUI with PyQt5: layouts, signals (`clicked`, `returnPressed`) and styling with `setObjectName` and stylesheets
- Keeping secrets out of a repository with `.gitignore`

## Possible next steps

- 5-day forecast
- Remembering the last searched city
- Switching between °C and °F
