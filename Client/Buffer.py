class Buffer:
    def __init__(self):
        self.cmd = ''
        self. content = ''

    def __len__(self):
        if self.cmd:
            return 1
        else:
            return 0

    def assign(self, cmd, content):
        self.cmd = cmd
        self.content = content

    def string(self):
        return self.cmd, self.content
