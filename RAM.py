KB = 1024

import sys

class RAM:
    def __init__(self):
        self.memory = bytearray(100)
    
    def read_bytes (self, start, size):
        return self.memory[start : start + size]
    
    def write_bytes (self, start, data: bytearray):
        self.memory[start:start + len(data)] = data