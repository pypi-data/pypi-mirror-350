import unittest
from qodex_recognition import main
import os

class TestCase(unittest.TestCase):
    def test_car_number_recognition(self):
        token = os.environ.get("mail_token")
        inst = main.MailNumberRecognitionRus()
        inst.set_token(token)
        with open("123.jpg", "rb") as fobj:
            res = inst.get_result(fobj)
            print(res)


if __name__ == "__main__":
    unittest.main()