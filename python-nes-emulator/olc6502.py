from Bus import Bus
import numpy as np

class Instruction:
    def __init__(self, name: str, operate: np.uint8(), addrmode: np.uint8(), cycles: np.uint8()):
        self.name = name
        self.operate = operate
        self.addrmode = addrmode
        self.cycles = cycles

class olc6502:
    def __init__(self):
        # Bits of the status reg
        self.FLAGS6502 = {
            "C" : (1 << 0),	# Carry Bit
            "Z" : (1 << 1),	# Zero
            "I" : (1 << 2),	# Disable Interrupts
            "D" : (1 << 3),	# Decimal Mode (unused)
            "B" : (1 << 4),	# Break
            "U" : (1 << 5),	# Unused
            "V" : (1 << 6),	# Overflow
            "N" : (1 << 7),	# Negative
        }

        self.a = np.uint8(0x00) # Accumulator
        self.x = np.uint8(0x00) # X Register
        self.y = np.uint8(0x00) # Y Register
        self.stkp = np.uint8(0x00) # Stack Pointer
        self.pc = np.uint16(0x0000) # Program Counter
        self.status = np.uint8(0x00) # Status register

        self.fetched = np.uint8(0x00) # Store fetched data

        self.addr_abs = np.uint16(0x0000) # Memory location to read from
        self.addr_rel = np.uint16(0x00)

        self.opcode = np.uint8(0x00)
        self.cycles = np.uint8(0) # Cycles left for instruction

        # Holds all instructions
        self.lookup = [
                        Instruction("BRK",self.BRK,self.IMM,7),Instruction("ORA",self.ORA,self.IZX,6),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,3),Instruction("ORA",self.ORA,self.ZP0,3),Instruction("ASL",self.ASL,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("PHP",self.PHP,self.IMP,3),Instruction("ORA",self.ORA,self.IMM,2),Instruction("ASL",self.ASL,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.NOP,self.IMP,4),Instruction("ORA",self.ORA,self.ABS,4),Instruction("ASL",self.ASL,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BPL",self.BPL,self.REL,2),Instruction("ORA",self.ORA,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("ORA",self.ORA,self.ZPX,4),Instruction("ASL",self.ASL,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("CLC",self.CLC,self.IMP,2),Instruction("ORA",self.ORA,self.ABY,4),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("ORA",self.ORA,self.ABX,4),Instruction("ASL",self.ASL,self.ABX,7),Instruction("???",self.XXX,self.IMP,7),
                        Instruction("JSR",self.JSR,self.ABS,6),Instruction("AND",self.AND,self.IZX,6),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("BIT",self.BIT,self.ZP0,3),Instruction("AND",self.AND,self.ZP0,3),Instruction("ROL",self.ROL,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("PLP",self.PLP,self.IMP,4),Instruction("AND",self.AND,self.IMM,2),Instruction("ROL",self.ROL,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("BIT",self.BIT,self.ABS,4),Instruction("AND",self.AND,self.ABS,4),Instruction("ROL",self.ROL,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BMI",self.BMI,self.REL,2),Instruction("AND",self.AND,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("AND",self.AND,self.ZPX,4),Instruction("ROL",self.ROL,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("SEC",self.SEC,self.IMP,2),Instruction("AND",self.AND,self.ABY,4),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("AND",self.AND,self.ABX,4),Instruction("ROL",self.ROL,self.ABX,7),Instruction("???",self.XXX,self.IMP,7),
                        Instruction("RTI",self.RTI,self.IMP,6),Instruction("EOR",self.EOR,self.IZX,6),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,3),Instruction("EOR",self.EOR,self.ZP0,3),Instruction("LSR",self.LSR,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("PHA",self.PHA,self.IMP,3),Instruction("EOR",self.EOR,self.IMM,2),Instruction("LSR",self.LSR,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("JMP",self.JMP,self.ABS,3),Instruction("EOR",self.EOR,self.ABS,4),Instruction("LSR",self.LSR,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BVC",self.BVC,self.REL,2),Instruction("EOR",self.EOR,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("EOR",self.EOR,self.ZPX,4),Instruction("LSR",self.LSR,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("CLI",self.CLI,self.IMP,2),Instruction("EOR",self.EOR,self.ABY,4),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("EOR",self.EOR,self.ABX,4),Instruction("LSR",self.LSR,self.ABX,7),Instruction("???",self.XXX,self.IMP,7),
                        Instruction("RTS",self.RTS,self.IMP,6),Instruction("ADC",self.ADC,self.IZX,6),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,3),Instruction("ADC",self.ADC,self.ZP0,3),Instruction("ROR",self.ROR,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("PLA",self.PLA,self.IMP,4),Instruction("ADC",self.ADC,self.IMM,2),Instruction("ROR",self.ROR,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("JMP",self.JMP,self.IND,5),Instruction("ADC",self.ADC,self.ABS,4),Instruction("ROR",self.ROR,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BVS",self.BVS,self.REL,2),Instruction("ADC",self.ADC,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("ADC",self.ADC,self.ZPX,4),Instruction("ROR",self.ROR,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("SEI",self.SEI,self.IMP,2),Instruction("ADC",self.ADC,self.ABY,4),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("ADC",self.ADC,self.ABX,4),Instruction("ROR",self.ROR,self.ABX,7),Instruction("???",self.XXX,self.IMP,7),
                        Instruction("???",self.NOP,self.IMP,2),Instruction("STA",self.STA,self.IZX,6),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,6),Instruction("STY",self.STY,self.ZP0,3),Instruction("STA",self.STA,self.ZP0,3),Instruction("STX",self.STX,self.ZP0,3),Instruction("???",self.XXX,self.IMP,3),Instruction("DEY",self.DEY,self.IMP,2),Instruction("???",self.NOP,self.IMP,2),Instruction("TXA",self.TXA,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("STY",self.STY,self.ABS,4),Instruction("STA",self.STA,self.ABS,4),Instruction("STX",self.STX,self.ABS,4),Instruction("???",self.XXX,self.IMP,4),
                        Instruction("BCC",self.BCC,self.REL,2),Instruction("STA",self.STA,self.IZY,6),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,6),Instruction("STY",self.STY,self.ZPX,4),Instruction("STA",self.STA,self.ZPX,4),Instruction("STX",self.STX,self.ZPY,4),Instruction("???",self.XXX,self.IMP,4),Instruction("TYA",self.TYA,self.IMP,2),Instruction("STA",self.STA,self.ABY,5),Instruction("TXS",self.TXS,self.IMP,2),Instruction("???",self.XXX,self.IMP,5),Instruction("???",self.NOP,self.IMP,5),Instruction("STA",self.STA,self.ABX,5),Instruction("???",self.XXX,self.IMP,5),Instruction("???",self.XXX,self.IMP,5),
                        Instruction("LDY",self.LDY,self.IMM,2),Instruction("LDA",self.LDA,self.IZX,6),Instruction("LDX",self.LDX,self.IMM,2),Instruction("???",self.XXX,self.IMP,6),Instruction("LDY",self.LDY,self.ZP0,3),Instruction("LDA",self.LDA,self.ZP0,3),Instruction("LDX",self.LDX,self.ZP0,3),Instruction("???",self.XXX,self.IMP,3),Instruction("TAY",self.TAY,self.IMP,2),Instruction("LDA",self.LDA,self.IMM,2),Instruction("TAX",self.TAX,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("LDY",self.LDY,self.ABS,4),Instruction("LDA",self.LDA,self.ABS,4),Instruction("LDX",self.LDX,self.ABS,4),Instruction("???",self.XXX,self.IMP,4),
                        Instruction("BCS",self.BCS,self.REL,2),Instruction("LDA",self.LDA,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,5),Instruction("LDY",self.LDY,self.ZPX,4),Instruction("LDA",self.LDA,self.ZPX,4),Instruction("LDX",self.LDX,self.ZPY,4),Instruction("???",self.XXX,self.IMP,4),Instruction("CLV",self.CLV,self.IMP,2),Instruction("LDA",self.LDA,self.ABY,4),Instruction("TSX",self.TSX,self.IMP,2),Instruction("???",self.XXX,self.IMP,4),Instruction("LDY",self.LDY,self.ABX,4),Instruction("LDA",self.LDA,self.ABX,4),Instruction("LDX",self.LDX,self.ABY,4),Instruction("???",self.XXX,self.IMP,4),
                        Instruction("CPY",self.CPY,self.IMM,2),Instruction("CMP",self.CMP,self.IZX,6),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("CPY",self.CPY,self.ZP0,3),Instruction("CMP",self.CMP,self.ZP0,3),Instruction("DEC",self.DEC,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("INY",self.INY,self.IMP,2),Instruction("CMP",self.CMP,self.IMM,2),Instruction("DEX",self.DEX,self.IMP,2),Instruction("???",self.XXX,self.IMP,2),Instruction("CPY",self.CPY,self.ABS,4),Instruction("CMP",self.CMP,self.ABS,4),Instruction("DEC",self.DEC,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BNE",self.BNE,self.REL,2),Instruction("CMP",self.CMP,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("CMP",self.CMP,self.ZPX,4),Instruction("DEC",self.DEC,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("CLD",self.CLD,self.IMP,2),Instruction("CMP",self.CMP,self.ABY,4),Instruction("NOP",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("CMP",self.CMP,self.ABX,4),Instruction("DEC",self.DEC,self.ABX,7),Instruction("???",self.XXX,self.IMP,7),
                        Instruction("CPX",self.CPX,self.IMM,2),Instruction("SBC",self.SBC,self.IZX,6),Instruction("???",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("CPX",self.CPX,self.ZP0,3),Instruction("SBC",self.SBC,self.ZP0,3),Instruction("INC",self.INC,self.ZP0,5),Instruction("???",self.XXX,self.IMP,5),Instruction("INX",self.INX,self.IMP,2),Instruction("SBC",self.SBC,self.IMM,2),Instruction("NOP",self.NOP,self.IMP,2),Instruction("???",self.SBC,self.IMP,2),Instruction("CPX",self.CPX,self.ABS,4),Instruction("SBC",self.SBC,self.ABS,4),Instruction("INC",self.INC,self.ABS,6),Instruction("???",self.XXX,self.IMP,6),
                        Instruction("BEQ",self.BEQ,self.REL,2),Instruction("SBC",self.SBC,self.IZY,5),Instruction("???",self.XXX,self.IMP,2),Instruction("???",self.XXX,self.IMP,8),Instruction("???",self.NOP,self.IMP,4),Instruction("SBC",self.SBC,self.ZPX,4),Instruction("INC",self.INC,self.ZPX,6),Instruction("???",self.XXX,self.IMP,6),Instruction("SED",self.SED,self.IMP,2),Instruction("SBC",self.SBC,self.ABY,4),Instruction("NOP",self.NOP,self.IMP,2),Instruction("???",self.XXX,self.IMP,7),Instruction("???",self.NOP,self.IMP,4),Instruction("SBC",self.SBC,self.ABX,4),Instruction("INC",self.INC,self.ABX,7),Instruction("???",self.XXX,self.IMP,7)
        ]

    def ConnectBus(self, bus: Bus()):
        self.bus = bus

    # Call the busses read
    def read(self, a: np.uint16()) -> np.uint8():
        return self.bus.read(a, False)

    # Call the busses write
    def write(self, a: np.uint16(), d: np.uint8()):
        self.bus.write(a, d)

    # Convenience functions to access status register
    def GetFlag(self, f: dict) -> np.uint8():
        None

    def SetFlag(self, f: dict, v: bool):
        None

    # Handle the clock
    def clock(self):
        if(self.cycles == 0):
            self.opcode = self.read(self.pc)
            self.pc += 1

            # Get starting number of cycles
            self.cycles = self.lookup[self.opcode].cycles
            self.lookup[self.opcode].addrmode()
            self.lookup[self.opcode].operate()

            # For additional cycles
            additional_cycle1 = np.uint8(self.lookup[self.opcode].addrmode())
            additional_cycle2 = np.uint8(self.lookup[self.opcode].operate())

            # If they need an additional clock cycle
            self.cycles += (additional_cycle1 & additional_cycle2)
        
        self.cycles -= 1
    
    def reset(self):
        None

    def irq(self):
        None
    
    def nmi(self):
        None

    def fetch(self) -> np.uint8():
        None

    # Addressing Modes

    # Implied - No data in instruction; Operating on the accumulator
    def IMP(self) -> np.uint8():
        self.fetched = self.a
        return 0
    
    # Immediate Mode - Data is part of instruction
    def IMM(self) -> np.uint8():
        self.addr_abs = (self.pc + 1)
        return 0

    # Zero page addressing
    def ZP0(self) -> np.uint8():
        self.addr_abs = self.read(self.pc)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0

    # Zero page addressing - Offset from X
    def ZPX(self) -> np.uint8():
        self.addr_abs = self.read(self.pc + self.x)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0
    
    # Zero page addressing - Offset from Y
    def ZPY(self) -> np.uint8():
        self.addr_abs = self.read(self.pc + self.y)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0

    # Absolute Address
    def ABS(self) -> np.uint8():
        self.lo = np.uint16(self.read(self.pc))
        self.pc += 1
        self.hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (self.hi << 8) | self.lo

        return 0

    # Absolute Address - X Offset
    def ABX(self) -> np.uint8():
        self.lo = np.uint16(self.read(self.pc))
        self.pc += 1
        self.hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (self.hi << 8) | self.lo
        self.addr_abs += self.x
        
        if ((self.addr_abs & 0xFF00) != (self.hi << 8)):
            return 1  
        else:
            return 0

    # Absolute Address - Y Offset
    def ABY(self) -> np.uint8():
        self.lo = np.uint16(self.read(self.pc))
        self.pc += 1
        self.hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (self.hi << 8) | self.lo
        self.addr_abs += self.y
        
        if ((self.addr_abs & 0xFF00) != (self.hi << 8)):
            return 1  
        else:
            return 0

    # Indirect Addressing
    def IND(self) -> np.uint8():
        self.ptr_lo = np.uint16(self.read(self.pc))
        self.pc += 1
        self.ptr_hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.ptr = np.uint16(self.ptr_hi << 8) | self.ptr_lo

        self.addr_abs = (self.read(self.ptr + 1) << 8) | self.read(self.ptr + 0)

        return 0

    # Opcodes

    # Catch an illegal opcode