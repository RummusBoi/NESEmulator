from abc import ABC, abstractmethod
from RAM import *
from ROM import *
import CPU

class Instruction(ABC):

    @abstractmethod
    def execute(self, opcode: bytearray, p: bytearray, ram: RAM):
        pass

#lambda functions for getting value from memory, sorted by 
# (Indirect, X) 
# Zero page 
# Immediate  
# Absolute 
# (Indirect), Y 
# Zero page, X 
# Absolute, Y 
# Absolute, X)

getMemArray = [
    lambda cpu, nextbytes: [((cpu.ram.read_bytes(getMemArray[0](cpu, nextbytes), 1))[0] + (cpu.ram.read_bytes((nextbytes[0] + cpu.X + 1))[0] % 256, 1)) * 256, 2],
    lambda cpu, nextbytes: [(nextbytes[0]), 2],
    lambda cpu, nextbytes: [(cpu.PC - 1), 2], #TODO might not work #TODO assumes that the program counter has been incremented
    lambda cpu, nextbytes: [(nextbytes[0] << 8 + nextbytes[1][0]), 3],
    lambda cpu, nextbytes: [((cpu.ram.read_bytes(nextbytes[0], 1))[0] + (cpu.ram.read_bytes((nextbytes[0] + 1) % 256, 1))[0] * 256 + cpu.Y), 2],
    lambda cpu, nextbytes: [(nextbytes[0] + cpu.X) % 256, 2],
    lambda cpu, nextbytes: [(nextbytes[0] + cpu.Y), 3],
    lambda cpu, nextbytes: [(nextbytes[0] + cpu.X), 3]
    ]

def ALUMemHelper(f, opcode: bytes, cpu: CPU.CPU):
    #find the addressing mode of this operation. The addressing mode for the ALU operations are stored in bit 2, 3 and 4.
    code = (opcode & 0b11100) >> 2
    
    #use the helper function to retrieve the byte from memory
    print("Counter: " + str(cpu.PC))
    print(cpu.instructions[0:100])
    nextbytes = cpu.instructions[cpu.PC + 1:cpu.PC + 1 + 2]
    try:
        print("Next bytes: " + str(nextbytes[0]) + " : " + str(nextbytes[1]))
    except:
        print("Next bytes: " + str(nextbytes[0]))
    
    print("code: " + str(code))
    val = getMemArray[code](cpu, nextbytes)
    print("Memory address to be accessed: " + str(val[0]))

    cpu.PC += val[1]
    val = cpu.ram.read_bytes(val[0], 1)
    print("Val retrieved from memory: " + str(val))

    #perform the ALU operation on the retrieved byte
    result = f(cpu.A, val[0])
    print("Result: " + str(result))

    #save result to accumulator
    cpu.A = result    

    #TODO where should processor status be updated?


#ALU instructions. Instructions whose least significant bits are (01)

class ORA(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): #TODO might need additional arguments, such as cpu.P
        ALUMemHelper (lambda a, b: a | b, opcode, cpu)

class ADC(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): #TODO might need additional arguments, such as cpu.P
        ALUMemHelper (lambda a, b: a + b, opcode, cpu)