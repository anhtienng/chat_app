class Buffer:
    def __init__(self, lock):
        self.lock = lock
        self.cmd = ''
        self. content = ''

    def __len__(self):
        if self.cmd:
            return 1
        else:
            return 0

    def assign(self, cmd, content):
        self.lock.acquire()
        self.cmd = cmd
        self.content = content
        self.lock.release()

    def string(self):
        return self.cmd, self.content
