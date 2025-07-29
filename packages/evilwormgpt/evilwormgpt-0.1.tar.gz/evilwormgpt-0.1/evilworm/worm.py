import requests
import urllib.parse

class EvilWorm:
    def __init__(self):
        self.base_url = "https://hamza.serveo.net/api/worm?txt="
        self.headers = {
            'Accept': "*/*",
            'User-Agent': "Mozilla/5.0",
            'X-Requested-With': "XMLHttpRequest"
        }
        self.chat_log = ""

    def ask(self, prompt: str) -> str:
        self.chat_log += f"user: {prompt}\n"
        payload = self.chat_log + "ai:"
        encoded = urllib.parse.quote(payload)

        res = requests.get(self.base_url + encoded, headers=self.headers)
        reply = res.text.strip()

        self.chat_log += f"ai: {reply}\n"
        return reply

    def reset(self):
        self.chat_log = ""
