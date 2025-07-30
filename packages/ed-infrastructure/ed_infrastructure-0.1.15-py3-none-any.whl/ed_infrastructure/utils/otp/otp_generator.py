from random import randint

from ed_domain.utils.otp import ABCOtpGenerator


class OtpGenerator(ABCOtpGenerator[str]):
    def __init__(self, dev_mode: bool = False) -> None:
        super().__init__()
        self.dev_mode = dev_mode

    def generate(self) -> str:
        return (
            f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"
            if self.dev_mode is False
            else "0000"
        )
