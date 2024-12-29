from typing import List
class Memory:
    def __init__(self, size):
        self.memory = [None] * size

    def write(self, address, value) -> None:
        self.validAddress(address)
        self.memory[address] = value

    def read(self, address: int):
        self.validAddress(address)
        return self.memory[address]

    def validAddress(self, address) -> bool:
        if address <= self.MEMmax() and address >= 0:
            return True
        else:
            exit("FATAL: Memory adress out of range")

    def dump(self):
        return self.memory

    def MEMmax(self) -> int:
        return (len(self.memory)-1)
