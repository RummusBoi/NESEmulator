from RAM import *
from ROM import *
import Instruction

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

        self.ram = ram

        self.ram.write_bytes(0, bytearray(len(ram.memory)))

    def executeProgram (self, instructions: bytes):
        self.instructions = instructions
        self.PC = 0
        instructionArr = [Instruction.ADC(), Instruction.ORA()]
        print("Running program: \n" + str(instructions))
        while (self.PC >= 0 and self.PC < len(instructions)):
            print("Current instruction: " + str(self.PC) + " : " + str(int(instructions[self.PC])))
            instructionArr[0].execute(instructions[self.PC], self)