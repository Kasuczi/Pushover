import http.client
import urllib
import time
import logging


class PushoverNotifier:
    def __init__(self, app_token, user_key):
        self.app_token = app_token
        self.user_key = user_key

    def send_notification(self, message, title=None, url=None, url_title=None, priority=None, sound=None, retry_count=3, retry_delay=5):
        for attempt in range(retry_count):
            try:
                conn = http.client.HTTPSConnection("api.pushover.net:443")
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

                conn.request("POST", "/1/messages.json",
                             urllib.parse.urlencode(data),
                             {"Content-type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                return response.read()
            except http.client.RemoteDisconnected:
                logging.warning("Remote end disconnected. Retrying in {} seconds...".format(retry_delay))
                time.sleep(retry_delay)
            finally:
                conn.close()
        raise Exception("Failed to send notification after {} attempts".format(retry_count))
