from abc import ABC, abstractmethod
from RAM import *
from ROM import *
import CPU

bitch = 2

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
    #TODO this array needs to return OPERAND NOT ADDRESS. It is not known whether address belongs to ROM or RAM, which means that the 
    #value needs to be returned, not the address.
    lambda cpu, nextbytes: [((cpu.ram.read_bytes(getMemArray[0](cpu, nextbytes), 1))[0] + (cpu.ram.read_bytes((nextbytes[0] + cpu.X + 1))[0] % 256) * 256, 1), 2],
    lambda cpu, nextbytes: [(nextbytes[0]), 2],
    lambda cpu, nextbytes: [cpu.PC + 1, 2], #TODO might not work #TODO assumes that the program counter has been incremented
    lambda cpu, nextbytes: [(nextbytes[0] << 8 + nextbytes[1][0]), 3],
    lambda cpu, nextbytes: [((cpu.ram.read_bytes(nextbytes[0], 1))[0] + (cpu.ram.read_bytes((nextbytes[0] + 1) % 256)[0] * 256 + cpu.Y), 1), 2],
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

    if(code == 2):
        val = cpu.instructions[val[0]:val[0]+1]
    else:
        val = cpu.ram.read_bytes(val[0], 1)
    
    print("Val retrieved from memory: " + str(val))

    #perform the ALU operation on the retrieved byte
    result = f(cpu.A, val[0])
    print("Result: " + str(result))

    #TODO: not sure of the exact functionality of the carry bit. Should it be cleared if no carry occurs in bit 7?

    #set cpu flags
    if not (opcode >> 7 == 1):
        fresult = result%256
        carry = result > fresult
        cpu.P = (cpu.P & 0b01111100) | carry | ((fresult == 0) << 1) | (fresult & 0b10000000)
        result = fresult

    #save result to accumulator
    cpu.A = result    

#ALU instructions. Instructions whose least significant bits are (01)

class ORA(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        ALUMemHelper (lambda a, b: a | b, opcode, cpu)

class ADC(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        ALUMemHelper (lambda a, b: a + b, opcode, cpu)

class AND(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        ALUMemHelper (lambda a, b: a & b, opcode, cpu)
        
class EOR(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        ALUMemHelper (lambda a, b: a ^ b, opcode, cpu)
        
class STA(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        code = (opcode & 0b11100) >> 2
        cpu.ram.write_bytes(getMemArray[code], cpu.A)
    
class LDA(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        ALUMemHelper (lambda a, b: b, opcode, cpu)

class CMP(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        code = (opcode & 0b11100) >> 2
        nextbytes = cpu.instructions[cpu.PC + 1:cpu.PC + 1 + 2]

        val = getMemArray[code](cpu, nextbytes)
        cpu.PC += val[1]

        #TODO: consider the use of if-statements here:
        
        if(cpu.A >= val[0]):
            if(cpu.A == val[0]):
                cpu.P = (cpu.P & 0b11111100) | 0b11
            else:
                cpu.P = (cpu.P & 0b11111100) | 0b01
        
class LDA(Instruction):
    def execute(self, opcode: bytes, cpu: CPU): 
        carryflag = 1
        ALUMemHelper (lambda a, b: a - b - (1 - carryflag), opcode, cpu)

# ------------------------- END OF ALU INSTRUCTIONS ------------------------- #

# ------------------------- START OF CONTROL INSTRUCTIONS ------------------------- #

# memory function for getting memory content for control operations. Ordering is the following:

getMemArray = [
    lambda cpu, nextbytes: [(cpu.PC + 1), 2],
    lambda cpu, nextbytes: [(nextbytes[0]), 2],
    lambda cpu, nextbytes: [0x0, 2],
    lambda cpu, nextbytes: [(nextbytes[0] << 8 + nextbytes[1][0]), 3],
    lambda cpu, nextbytes: [,2]
]