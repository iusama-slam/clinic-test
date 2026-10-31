"""The sending boundary. Only the console sender exists today."""


class ConsoleSender:
    def send(self, phone: str, text: str) -> None:
        print(f"SMS to {phone}: {text}")
