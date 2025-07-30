import http.client
import json

from ed_domain.utils.sms.abc_sms_sender import ABCSmsSender


class SmsSender(ABCSmsSender):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def send(self, recipient: str, message: str) -> None:
        """Send an SMS message to the specified recipient.

        Args:
            recipient: The phone number to send the SMS to
            message: The content of the SMS message

        Raises:
            Exception: If the SMS fails to send
        """
        conn = None
        try:
            conn = http.client.HTTPSConnection("kq13q8.api.infobip.com")
            payload = json.dumps(
                {
                    "messages": [
                        {
                            "destinations": [{"to": recipient}],
                            "from": "ServiceSMS",
                            "text": message,
                        }
                    ]
                }
            )
            headers = {
                "Authorization": f"App {self._api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            conn.request("POST", "/sms/2/text/advanced", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            if res.status < 200 or res.status >= 300:
                raise Exception(f"Failed to send SMS: {data}")
        finally:
            if conn:
                conn.close()
