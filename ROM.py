import sys
KB = 1024

class ROM:
    def __init__(self):
        self.data = []
        pass

    def read_data (self, path):
        with open(path, 'rb') as nes:
            self.data = nes.read()
            
            romPointer = 0

            self.header = self.read_bytes(0, 16)

            romPointer = 16

            #reads and sets flag variables for this ROM:
            self.setup_flags()
            
            if(self.FLAGS[0][1] == 1):
                self.trainer = self.read_bytes(16, 512)
                romPointer = 16 + 512 + 1
            else:
                self.trainer = []

            self.prgROM = self.read_bytes(romPointer, self.read_bytes(4, 1)[0] * 16 * KB)
            romPointer += self.read_bytes(4, 1)[0] * 16 * KB 
            self.chrROM = self.read_bytes(romPointer, self.read_bytes(5, 1)[0] * 8 * KB)
            romPointer += self.read_bytes(5, 1)[0] * 8 * KB
            


    def read_bytes(self, start, size):
        return self.data[start:start + size]
    
    def to_bits(self, byte: bytes):
        return bin(byte)
            
    def setup_flags(self):
        self.FLAGS = [bin(self.read_bytes(i, 1)[0]) for i in range (6, 12)]

    def write_bytes(self, start, data: bytearray):
        #should not be used under normal circumstances
        #TODO this function is unusable
        self.data[start:start + len(data)] = data