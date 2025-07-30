import resend
from ed_domain.utils.email.abc_email_sender import ABCEmailSender


class EmailSender(ABCEmailSender):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def send(self, sender: str, recipient: str, subject: str, html: str) -> None:
        resend.api_key = self._api_key
        resend.Emails.send(
            {
                "from": sender,
                "to": recipient,
                "subject": subject,
                "html": html,
            }
        )
