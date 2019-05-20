KB = 1024

import sys

class RAM:
    def __init__(self):
        self.memory = bytearray(100)
    
    def read_bytes (self, start: int, size: int):
        end = start + size
        return self.memory[start:end]
    
    def write_bytes (self, start, data: bytearray):
        self.memory[start:start + len(data)] = data