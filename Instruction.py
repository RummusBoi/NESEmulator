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

#lambda functions for getting value from memory, sorted by (d,x : d,y : a,x : a,y : (d,x) : (d),y)
getMemArray = [
    #
    lambda cpu, nextbytes: (cpu.ram.read_bytes(getMemArray[0](cpu, nextbytes), 1) + cpu.ram.read_bytes((nextbytes[0][0] + cpu.X + 1) % 256, 1)) * 256,
    lambda cpu, nextbytes: (nextbytes[0][0]),
    lambda cpu, nextbytes: (cpu.PC - 1), #TODO might not work #TODO assumes that the program counter has been incremented
    lambda cpu, nextbytes: (nextbytes[0][0] << 8 + nextbytes[1][0]),
    lambda cpu, nextbytes: (cpu.ram.read_bytes(nextbytes[0][0], 1) + cpu.ram.read_bytes((nextbytes[0][0] + 1) % 256, 1) * 256 + cpu.Y),
    lambda cpu, nextbytes: (nextbytes[0][0] + cpu.X) % 256,
    lambda cpu, nextbytes: (nextbytes[0][0] + cpu.Y),
    lambda cpu, nextbytes: (nextbytes[0][0] + cpu.X)

    #TODO reorder these such they fit the correct opcodes.
    #TODO add the remaining addressing modes, might not need (d,y) mode for ALU.
    ]

def ALUMemHelper(f, opcode: bytearray, cpu: CPU.CPU):
    #find the addressing mode of this operation. The addressing mode for the ALU operations are stored in bit 2, 3 and 4.
    code = opcode & 11100

    #use the helper function to retrieve the byte from memory

    nextbytes = cpu.ram.read_bytes(cpu.PC, 2) #TODO assumes the program counter has already been incremented
    val = cpu.ram.read_bytes(getMemArray[code](cpu, nextbytes), 1)

    #perform the ALU operation on the retrieved byte
    result = f(cpu.A, val)

    #save result to accumulator
    cpu.A += result    

    #TODO where should processor status be updated?
    #TODO where should


#ALU instructions. Instructions whose least significant bits are (01)

class ORA(Instruction):
    def __init__(self):
        self.value = 2
    def execute(self, opcode: bytearray, p: bytearray, ram: RAM, pc):
        ALUMemHelper (lambda a, b: a | b)