from abc import ABC, abstractmethod
from RAM import *
import CPU

class Instruction(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def execute(self, opcode: bytearray, p: bytearray, ram: RAM):
        pass

def getMemoryLocation(opcode: bytearray)

class ADC(Instruction):
    def __init__(self):
        self.value = 2
    
    def execute(self, opcode: bytearray, cpu: CPU.CPU):
        if(opcode == 0x69):
            
            