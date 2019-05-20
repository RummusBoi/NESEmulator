import argparse
from ROM import *
from RAM import *
from Instruction import *
from CPU import *

def main ():

    parser = argparse.ArgumentParser(description = "NES Emulator.")
    parser.add_argument ('rom_path', metavar = 'ROM path', type=str, help='path to nes rom')
    
    args = parser.parse_args()
    
    print("Path to ROM: " + args.rom_path)

    rom = ROM()
    rom.read_data(args.rom_path)
    for i in rom.read_bytes(0, 100):
        print(i)

    

    ram = RAM()

    cpu = CPU()
    cpu.start_up(ram)

    cpu.A = 0
    cpu.PC = 16

    instr = ADC()

    cpu.ram.write_bytes(0, bytearray([3, 2]))

    print("Before execution: " + str(cpu.A))
    cpu.executeProgram (rom.read_bytes(16, 4))
    print("After execution: " + str(cpu.A))

if __name__ == "__main__": 
    main()