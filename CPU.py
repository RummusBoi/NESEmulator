from RAM import *


class CPU:
    def __init__(self):
        self.A = bytearray(1)
        self.X = bytearray(1)
        self.Y = bytearray(1)
        self.PC = 0
        self.S = bytearray(1)
        
        #Status flags used by the alu. Only 6 bits are used
        self.P = bytearray(1) 
        
        
    
    def start_up(self, ram: RAM):
        self.A = 0
        self.X = 0
        self.Y = 0
        self.P = 0x34
        self.S = 0xFD

        ram.write_bytes(0, bytearray(len(ram)))

