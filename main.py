import argparse
from ROM import *
from RAM import *
from Instruction import *

def main ():
    print ("Hello world")

    parser = argparse.ArgumentParser(description = "NES Emulator.")
    parser.add_argument ('rom_path', metavar = 'ROM path', type=str, help='path to nes rom')
    
    args = parser.parse_args()
    
    print("Path to ROM: " + args.rom_path)

    rom = ROM()
    rom.read_data(args.rom_path)

    print(rom.header)

    ram = RAM()

    instr = ADC()
    print(instr.execute(bytearray(0)))

if __name__ == "__main__": 
    main()