class Buffer:
    def __init__(self, name):
        self.name = name
        self.buffer = []

    def write(self, value):
        self.buffer.append(value)
        return(value)

    def read(self):
        return(self.buffer.pop(0))

    def size(self):
        return(len(self.buffer))

    def dump(self):
        return self.name, self.buffer
