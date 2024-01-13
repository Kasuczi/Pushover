import http.client
import urllib


class PushoverNotifier:
    def __init__(self, app_token, user_key):
        self.app_token = app_token
        self.user_key = user_key
        self.conn = http.client.HTTPSConnection("api.pushover.net:443")

    def send_notification(self, message, title=None, url=None, url_title=None, priority=None, sound=None):
        data = {
            "token": self.app_token,
            "user": self.user_key,
            "message": message
        }

        if title:
            data["title"] = title
        if url:
            data["url"] = url
        if url_title:
            data["url_title"] = url_title
        if priority:
            data["priority"] = priority
        if sound:
            data["sound"] = sound

        self.conn.request("POST", "/1/messages.json",
                          urllib.parse.urlencode(data),
                          {"Content-type": "application/x-www-form-urlencoded"})
        response = self.conn.getresponse()
        return response.read()


if __name__ == "__main__":
    app_token = ""
    user_key = ""

    notifier = PushoverNotifier(app_token, user_key)
    response = notifier.send_notification("TEST123", title="Test")
