class register:
    def __init__(self, name):
        self.name = name
        self.value = 0
    
    def do(self, action, value=None):
        if action == "write":
            self.value = value
            return(self.value)
        elif action == "read":
            return(self.value)
        elif action == "inc":
            self.value = self.value +1
            return(self.value)
        elif action == "dec":
            self.value = self.value -1
            return(self.value)
        else:
            exit("ERROR with register " + str(self.name) + action + str(value))
    
class buffer:
    def __init__(self, name):
        self.name = name
        self.buffer = []

    def do(self, action, value=None):
        if action == "write":
            self.buffer.append(value)
            return(value)
        elif action == "read":
            return(self.buffer.pop(0))
        elif action == "size":
            return(len(self.buffer))
        else:
            exit("ERROR with buffer: ", action)

    def dump(self):
        return self.name, self.buffer

    