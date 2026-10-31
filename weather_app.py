import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout)
from PyQt5.QtCore import Qt
from config import API_KEY



class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.details_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.details_label)

        self.setLayout(vbox)


        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.details_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.details_label.setObjectName("details_label")

        self.setStyleSheet("""
                    QLabel, QPushButton{
                        font-family: Calibri;
                    }
                    QLabel#city_label{
                        font-size: 40px;
                        font-style: Italic;
                    }
                    QLineEdit#city_input{
                        font-size: 40px;
                        min-height: 50px;
                    }
                    QPushButton#get_weather_button{
                        font-size: 30px;
                        font-weight: bold;
                    }
                    QLabel#temperature_label{
                        font-size: 75px;
                    }
                    QLabel#details_label{
                        font-size: 50px;
                    }
                    QLabel#emoji_label{
                        font-size: 100px;
                        font-family: Segoe UI emoji;
                    }
                    QLabel#description_label{
                        font-size: 50px;
                    }
                         """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):

        api_key = f"{API_KEY}"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl"

        
        if not city:
            self.display_error("Wpisz nazwę miasta")
            return

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request  timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the url")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")



    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")
        self.details_label.setText("")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet(f"font-size: 75px;")
        temperature = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        feeltemp = data["main"]["feels_like"]
        rh = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        color = self.get_temperature_color(temperature)
        self.temperature_label.setStyleSheet(f"font-size: 75px; background-color: {color};")



        self.temperature_label.setText(f"{temperature:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        self.details_label.setText(f"Odczuwalna: {feeltemp:.0f}°C | Wilgotnosc: {rh}% | Wiatr: {wind}m/s")

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "😶‍🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
    @staticmethod
    def get_temperature_color(temperature):
        if temperature <= 0:
            return "lightblue"
        elif 0 < temperature < 20:
            return "lightgreen"
        else:
            return "orange"
        


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_app = WeatherApp()
    Weather_app.show()
    sys.exit(app.exec_())
