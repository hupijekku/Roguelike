messages = []


def add_message(message):
    messages.append(message)


class LogMessage:

    def __init__(self, text, color):
        self.text = text
        self.color = color