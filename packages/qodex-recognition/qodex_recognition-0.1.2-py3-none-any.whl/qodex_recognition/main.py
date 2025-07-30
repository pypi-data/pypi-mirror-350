import traceback
from abc import ABC, abstractmethod
import requests
import json


class RecognitionService(ABC):
    @abstractmethod
    def recognise(self, photo, *args, **kwargs):
        return

    def get_result(self, photo, *args, **kwargs):
        result = self.recognise(photo, *args, **kwargs)
        if not result:
            return {'error': "Mail response waiting timeout expired!",
                    "status_code": 0,
                    "msg": result}
        if not isinstance(result, requests.Response):
            return {'error': "Unknown error!",
                    "status_code": 0,
                    "msg": "Mail response is not requests.Response"}
        if result.status_code != 200:
            return {'error': "Status code is not 200",
                    "status_code": result.status_code,
                    "msg": result}
        return self.parse_result(result.json())

    def parse_result(self, result):
        return result


class CloudRecognitionService(RecognitionService):
    host = None
    recognise_url = None


class Mail(CloudRecognitionService):
    token = None
    oauth_provider = "mcs"
    host = "https://smarty.mail.ru"
    car_number_recognition_link = "/api/v1/objects/detect"
    mode = None

    def set_token(self, token):
        self.token = token

    def recognise(self, photo, *args, **kwargs):
        full_link = self.host + self.car_number_recognition_link
        meta = {
            "mode": [
                self.mode
            ],
            "images": [
                {
                    "name": "file"
                }
            ]
        }
        if not self.has_internet():
            return {"error": "no internet connection!",}
        result = requests.post(
            url=full_link,
            params={
                "oauth_token": self.token,
                "oauth_provider": self.oauth_provider},
            files={'file': photo},
            data={"meta": json.dumps(meta)},
            timeout=(3,10))
        print("HELLO2")
        return result

    def has_internet(self, timeout=2):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            return True
        except OSError:
            return False


class MailNumberRecognition(Mail):
    mode = "car_number"
    rus = True

    def parse_result(self, result):
        try:
            labels = result["body"]["car_number_labels"][0]
            if not "labels" in labels:
                return {'error': 'Car number is not found'}
            return labels['labels'][0]
        except:
            return {'error': result}


class MailNumberRecognitionRus(MailNumberRecognition):
    def parse_result(self, result):
        response = super().parse_result(result)
        if 'error' in response:
            return response
        if 'rus' in response:
            return response['rus']
