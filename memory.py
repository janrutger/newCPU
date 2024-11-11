class  memory:
    def __init__(self, size):
        self.memory = [None] * size

    def do(self, action, address, value=None):
        if address > self.MEMmax():
            exit("FATAL: Memory adress out of range")
        elif action == "write":
            self.memory[address] = value
        elif action != "read":
            return("ERROR")
        return(self.memory[address])
    
    def dump(self):
        return self.memory
    
    def MEMmax(self):
        return (len(self.memory)-1)