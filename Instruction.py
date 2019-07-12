from abc import ABC, abstractmethod
from RAM import *
from ROM import *
import CPU

bitch = 2

class Instruction(ABC):

    @abstractmethod
    def execute(self, opcode: bytearray, cpu: CPU):
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
#TODO this needs to return VALUE at memory location, NOT the ADDRESS
getMemArray = [
    lambda cpu, nextbytes: [(cpu.PC + 1), 2],
    lambda cpu, nextbytes: [(nextbytes[0]), 2],
    lambda cpu, nextbytes: [0x0, 2],
    lambda cpu, nextbytes: [(nextbytes[0] << 8 + nextbytes[1][0]), 3],
    lambda cpu, nextbytes: [0x0,2], #relative addressing mode. Will be implemented in the individual instruction cases.
    lambda cpu, nextbytes: [(nextbytes[0] + cpu.X) % 256, 2],
    lambda cpu, nextbytes: [0x0, 2],
    lambda cpu, nextbytes: [(nextbytes[0] + cpu.X), 3]
]

def CTRgetval(opcode: bytes, cpu: CPU.CPU) -> bytes:
    code = (opcode & 0b11100) >> 2
    nextbytes = cpu.instructions[cpu.PC + 1:cpu.PC + 1 + 2]
    val = getMemArray[code](cpu, nextbytes)  
    return val

class PHP(Instruction):
    def execute(self, opcode, cpu):
        cpu.push(cpu.P)

class PLP(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.pop()

class BPL(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions(cpu.PC + 1)
        if(cpu.P & 0b00000010 == 0b00000010):
            cpu.PC += offset - 128
        else:
            cpu.PC += 2

class CLC(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P & 0b11111110

class JSR(Instruction):
    def execute(self, opcode, cpu):
        loc = cpu.instructions[self.pc + 1:self.pc + 3]
        cpu.push(self.pc + 2)
        self.pc = loc

class BIT(Instruction):
    def execute(self, opcode, cpu):
        #find the addressing mode of this operation.
        val = CTRgetval(opcode, cpu)
        overflowFlag = val & 0b01000000
        negativeFlag = val & 0b10000000
        cpu.P = (cpu.P & overflowFlag) | overflowFlag
        cpu.P = (cpu.P & negativeFlag) | negativeFlag
        if(val & cpu.A):
            cpu.P = 0b01000000 | cpu.P

class BMI(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions(cpu.PC + 1)
        if(cpu.P & 0b10000000 == 0b10000000):
            cpu.PC += offset - 128
        else:
            cpu.PC += 2

class SEC(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P & 0b10000000

class RTI(Instruction):
    def execute(self, opcode, cpu):
        newP = cpu.pop()
        newPC = cpu.pop()
        cpu.P = newP
        cpu.PC = newPC
    
class PHA(Instruction):
    def execute(self, opcode, cpu):
        cpu.push(cpu.A)

class PLA(Instruction):
    def execute(self, opcode, cpu):
        cpu.A = cpu.pop()

class JMP(Instruction):
    def execute(self, opcode, cpu):    
        loc = cpu.instruction[cpu.PC + 1] << 8 + cpu.instructions[cpu.PC + 2]
        if(opcode == 0x6C):
            newLoc = cpu.ram.read_bytes[loc, 2]
            loc = newLoc[0] << 8 + newLoc[1]
        
        cpu.PC = cpu.ram.read_bytes[loc, 1]

class BVC(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions(cpu.PC + 1)
        if(cpu.P & 0b01000000 == 0b00000000):
            cpu.PC += offset - 128
        else:
            cpu.PC += 2

class CLI(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P & 0b11111011

class RTS(Instruction):
    def execute(self, opcode, cpu):
        val = cpu.pop()
        cpu.PC = val - 1

class BVS(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions[cpu.PC + 1]
        if(cpu.P & 0b01000000 == 0b01000000):
            cpu.PC = cpu.PC + offset
        else:
            cpu.PC += 2

class SEI(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P | 0b00000100      

class STY(Instruction):
    def execute(self, opcode, cpu):
        address = CTRgetval(opcode, cpu)
        cpu.ram.write_bytes(address, cpu.Y)

class TYA(Instruction):
    def execute(self, opcode, cpu):
        cpu.A = cpu.Y
        if(A == 0):
            cpu.P = cpu.P | 0b00000010
        cpu.P = (cpu.P & 0b01111111) | (cpu.A & 0b10000000)


class SHY(Instruction):
    def execute(self, opcode, cpu):
        raise Exception("Instruction not implemented.")

class LDY(Instruction):
    def execute(self, opcode, cpu):
        val = cpu.ram.read_bytes(CTRgetval(opcode, cpu), 1)
        cpu.Y = val
        if(cpu.Y == 0):
            cpu.P = cpu.P | 0b00000010
        cpu.P = (cpu.P & 0b01111111) | (cpu.Y & 0b10000000)
    
class DEY(Instruction):
    def execute(self, opcode, cpu):
        cpu.Y -= 1
        if(cpu.Y == 0):
            cpu.p = cpu.P | 0b00000010
        cpu.P = (cpu.P & 0b01111111) | (cpu.Y & 0b10000000)

class BCC(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions[cpu.PC + 1]
        if(cpu.P & 0b10000000 == 0b00000000):
            cpu.PC = cpu.PC + offset
        else:
            cpu.PC += 2

class TAY(Instruction):
    def execute(self, opcode, cpu):
        cpu.Y = cpu.A

        if(cpu.Y == 0):
            cpu.P = cpu.P | 0b00000010
        cpu.P = (cpu.P & 0b01111111) | (cpu.Y & 0b10000000)

class BCS(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions[cpu.PC + 1]
        if(cpu.P & 0b10000000 == 0b10000000):
            cpu.PC = cpu.PC + offset
        else:
            cpu.PC += 2

class CLV(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P & 0b10111111

class CPY(Instruction):
    def execute(self, opcode, cpu):
        val = cpu.ram.read_bytes(CTRgetval(opcode, cpu), 1)
        if(cpu.Y >= val):
            cpu.P = cpu.P | 0b10000000
        else:
            cpu.P = cpu.P & 0b01111111
        if(cpu.Y == val):
            cpu.P = cpu.P | 0b01000000
        else:
            cpu.P = cpu.P & 0b01000000

class INY(Instruction):
    def execute(self, opcode, cpu):
        cpu.Y += 1

class INX(Instruction):
    def execute(self, opcode, cpu):
        cpu.X += 1

class BNE(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions[cpu.PC + 1]
        if(cpu.P & 0b00000010 == 0b00000000):
            cpu.PC = cpu.PC + offset
        else:
            cpu.PC += 2

class BEQ(Instruction):
    def execute(self, opcode, cpu):
        offset = cpu.instructions[cpu.PC + 1]
        if(cpu.P & 0b00000010 == 0b00000010):
            cpu.PC = cpu.PC + offset
        else:
            cpu.PC += 2

class CLD(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P & 0b11110111

class SED(Instruction):
    def execute(self, opcode, cpu):
        cpu.P = cpu.P | 0b00001000

class CPX(Instruction):
    def execute(self, opcode, cpu):
        val = cpu.ram.read_bytes(CTRgetval(opcode, cpu), 1)
        if(cpu.X >= val):
            cpu.P = cpu.P | 0b10000000
        else:
            cpu.P = cpu.P & 0b01111111
        if(cpu.X == val):
            cpu.P = cpu.P | 0b01000000
        else:
            cpu.P = cpu.P & 0b01000000


# ------------------------- END OF CONTROL INSTRUCTIONS ------------------------- #

# ------------------------- START OF BLUE INSTRUCTIONS ------------------------- #

#reuses the getMemArray from control instruction, since the memory access
#is similar.

class ASL(Instruction):
    def execute(self, opcode, cpu):
        val = cpu.ram.read_bytes(CTRgetval(opcode, cpu), 1)
        cpu.P = cpu.P & ()