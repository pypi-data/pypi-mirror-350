
import requests

class EvilWorm:
    def __init__(self):
        self.url = "https://hamza.serveo.net/api/worm?txt="
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'x-requested-with': "mark.via.gp",
        }
        self.log = ""

    def ask(self, msg):
        self.log += f"user: {msg}\nai:"
        response = requests.get(self.url + requests.utils.quote(self.log), headers=self.headers)
        reply = response.text.strip()
        self.log += reply + "\n"
        return reply

    def reset(self):
        self.log = ""
