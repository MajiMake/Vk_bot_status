import vk_api
import requests
import time
from __token import token
from random import randint
from datetime import datetime


class Bot_status:

    def __init__(self, counter, token):
        self.text = None
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.response = requests.get(
            'http://api.forismatic.com/api/1.0/',
            params={'method': 'getQuote',
                    'format': 'text',
                    'key': counter,
                    'lang': 'ru'
                    }
        )

    def __call__(self):
        self.quote()
        self.set_stat()

    def set_stat(self):
        self.vk_session.method('status.set', {'text': self.text})

    def quote(self):
        if self.response.ok:
            prt_resp = len(self.response.text)
            print(prt_resp)
            if prt_resp >= 140:
                return False
            else:
                self.text = self.response.text
        else:
            return False


def timer():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


while True:
    mag = Bot_status(randint(1, 999999), token=token)
    if mag.quote() is False:
        print('слишком длинная цитата', mag.response.text)
        time.sleep(10)
        continue
    else:
        mag()
        timer()
        time.sleep(3600)
