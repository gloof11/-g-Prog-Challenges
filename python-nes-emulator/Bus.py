from olc6502 import olc6502
import numpy as np

class Bus:
    def __init__(self):
        self.cpu = olc6502()
        self.ram = [0]*(64*1024)

        # Connect CPU to communication bus
        self.cpu.ConnectBus(self)
    
    def write(self, addr: np.uint16(), data: np.uint8()):
        # Guard ram with the full range of ram
        if (addr >= 0x0000 and addr <= 0xFFFF):
            self.ram[addr] = data

    def read(self, addr: np.uint16(), readonly=False) -> np.uint8():
        # Guard ram with the full range of ram
        if (addr >= 0x0000 and addr <= 0xFFFF):
            # Return the contents of ram for a given address
            return self.ram[addr]
        else:
            return 0x00