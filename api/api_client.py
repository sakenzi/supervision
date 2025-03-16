import requests
from PyQt6.QtWidgets import QMessageBox


class ApiClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def send_data(self, parent, data):
        try:
            response = requests.post(self.api_url, json=data, timeout=5)
            response.raise_for_status()
            print(f"Данные успешно отправлены на API: {response.status_code}")
            return True, response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Не удалось отправить данные на API: {str(e)} (URL: {self.api_url})"
            print(f"Ошибка отправки данных на API: {e}")
            QMessageBox.critical(parent, "Ошибка API", error_message)
            return False, {}