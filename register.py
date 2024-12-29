class Register:
    def __init__(self):
        self.value

    def write(self, value):
        self.value = value
        return(self.value)

    def read(self) -> int:
        return(self.value)

    def inc(self):
        self.value = self.value + 1
        return self.value

    def dec(self) -> int:
        self.value = self.value - 1
        return self.value

    def dump(self) -> int:
        return self.value
