class Buffer:
    def __init__(self):
        self.content = ''

    def __len__(self):
        return len(self.content)

    def assign(self, message):
        self.content = message

    def string(self):
        return self.content
