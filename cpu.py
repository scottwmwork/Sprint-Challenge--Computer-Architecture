"""CPU functionality."""

import sys
import datetime

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Memory
        self.ram = [0] * 256
        # Registers
        self.reg = [0] * 7 
        
        # Opcode Values
        ADD   = 0b10100000
        MULT  = 0b10100010
        PRINT = 0b01000111
        LDI   = 0b10000010
        HLT   = 0b00000001
        PUSH  = 0b01000101
        POP   = 0b01000110
        CALL  = 0b01010000
        RET   = 0b00010001
        CMP   = 0b10100111
        JMP   = 0b01010100
        JEQ   = 0b01010101
        JNE   = 0b01010110
        ADDI  = 0b10001000 # Could not find opcode in spec so I included opcode from MIPS sheet
        ST    = 0b10000100

        # Add Opcodes to a branchtable
        self.branchtable = {}
        self.branchtable[ADD]   = self.add
        self.branchtable[MULT]  = self.mult
        self.branchtable[PRINT] = self.prn
        self.branchtable[LDI]   = self.ldi
        self.branchtable[HLT]   = self.hlt
        self.branchtable[POP]   = self.pop
        self.branchtable[PUSH]  = self.push
        self.branchtable[LDI]   = self.ldi
        self.branchtable[CALL]  = self.call
        self.branchtable[RET]   = self.ret
        self.branchtable[CMP]   = self.cmp
        self.branchtable[JMP]   = self.jmp
        self.branchtable[JEQ]   = self.jeq
        self.branchtable[JNE]   = self.jne 
        self.branchtable[ADDI]  = self.addi
        self.branchtable[ST]    = self.st

        # Program Counter
        self.PC = 0
        # Instruction Register
        self.IR = 0
        # Stack Pointer
        self.SP = len(self.ram) - 1
        # Flag
        self.FL = 0b00000000

    def load(self, program = None):
        """Load a program into Memory/Ram"""

        address = 0

        # This program is loaded in case there is no arguments specified
        program = [
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        
        # If arguements are specified
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
            program = open(file_name)
            program = program.read().split("\n")
            new_program = []

            # Cleaning .ls8 file
            for string in program:

                # Ignore comments
                if "#" in string:
                    string = string.split("#")[0]
                
                # Ignore empty lines
                if string != '':
                    new_program.append(string)

            program = new_program

            for instruction in program:
                self.ram[address] = int(instruction, 2)
                address += 1
        else:
            for instruction in program:
                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "AND":
            and_result = self.reg[reg_a] & self.reg[reg_b]
            self.reg[reg_a] = and_result
        elif op == "OR":
            or_result = self.reg[reg_a] | self.reg[reg_b]
            self.reg[reg_a] = or_result
        elif op == "XOR":
            xor_result = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = xor_result
        elif op == "NOT":
            not_result =  ~ self.reg[reg_a]
            self.reg[reg_a] = not_result
        elif op == "SHL":
            shl_result = self.reg[reg_a] << self.reg[reg_b]
            self.reg[reg_a] =shl_result
        elif op == "SHR":
            shr_result = self.reg[reg_a] >> self.reg[reg_b]
            self.reg[reg_a] = shr_result
        elif op == "MOD":
            mod_result = self.reg[reg_a] % self.reg[reg_b]
            self.reg[reg_a] = mod_result
        else:
            raise Exception("Unsupported ALU operation")

    def mult(self,reg_a, reg_b):
        """
        places the product of reg_a and reg_b into reg_a
        """
        self.reg[reg_a] *= self.reg[reg_b]
        self.PC += 3

    def add(self, reg_a, reg_b):
        """
        places the sum of reg_a and reg_b into reg_a
        """
        # References alu to complete operation
        self.alu("ADD", reg_a, reg_b)
        # Increment Program Counter
        self.PC += 3

    def sub(self, reg_a, reg_b):
        self.alu("SUB", reg_a, reg_b)
        self.PC += 3

    def subtract(self, reg_a, reg_b):
        """
        places the difference between reg_a and reg_b in reg_a
        """
        # Reference the alu to complete operation
        self.alu("SUB", reg_a, reg_b)
        # Increment Program Counter
        self.PC += 3

    def prn(self, reg_a, dontcare):
        """
        print value in reg_a
        """
        print(self.reg[reg_a])
        # Increment Program Counter
        self.PC += 2

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(address):
        """
        Reads value from memory
        """
        return self.ram[address]

    def ram_write(address, value):
        """
        Writes value to memory
        """
        self.ram[address] = value

    def hlt(self, dontcare1, dontcare2):
        """
        Stops Program
        """
        quit()

    def push(self, reg_a, doncare = None):
        """
        Used for stack
        """
        # Get value
        val = self.reg[reg_a]
        # Copy the value in the given register to the address pointed 
        self.ram[self.SP] = val
        # Decrement the Stack Pointer
        self.SP -= 1
        # Increase Program counter
        self.PC += 2
    
    def pop(self, reg_a, doncare = None):
        """
        Used for stack
        """
        # Get value
        val = self.ram[self.SP + 1]
        # copy the value from the address pointed to by SP to the given register
        self.reg[reg_a] = val
        # Remove value from memory
        self.ram[self.SP + 1] = 0
        # Increment Stack Pointer
        self.SP += 1
        # Increment Program Counter
        self.PC += 2

        return val

    def ldi(self, reg_a, val):
        """
        Set reg_a to equal val
        """
        # Set Register to Value
        self.reg[reg_a] = val
        # Increment Program Counter
        self.PC += 3

    def call(self, reg_a, doncare = None):
        #TODO
        # Load PC into a register
        self.reg[5] = self.PC + 2
        self.push(5)
        # set PC to address in memory
        self.PC = self.reg[reg_a]

    def ret(self, reg_a, reg_b):
        """
        Returns to previous place in memory address
        """    
        # Load old PC value from stack
        PC_val = self.pop(5)
        # Set current PC to old PC value
        self.PC = PC_val

    def st(self, reg_a, reg_b):
    	val = self.reg[reg_b]
    	self.ram_write(self.reg[reg_a], val)

    def cmp(self, reg_a, reg_b):
        if self.reg[reg_a] > self.reg[reg_b]:
            self.FL = 0b00000010
        elif self.reg[reg_a] < self.reg[reg_b]:
            self.FL = 0b00000100
        elif self.reg[reg_a] == self.reg[reg_b]:
            self.FL = 0b00000001
        
        self.PC += 3
            
    def jmp(self, reg_a, reg_b = None):
        """
        Sets PC to the address within reg_a
        """
        self.PC = self.reg[reg_a]

    def jeq(self, reg_a, reg_b):
        """
        If the FL flag indicates values are equal, call jmp instruction
        """
        if self.FL == 0b00000001:
            self.jmp(reg_a)
        else:
            self.PC += 2
            
    def jne(self, reg_a, reg_b):
        """
        If the FL flag indicates values are not equal, call jmp instruction
        """
        if self.FL == 0b00000010 or self.FL == 0b00000100:
            self.jmp(reg_a)
        else:
            self.PC += 2

    def addi(self, reg_a, val):
    	self.reg[reg_a] += val
    	self.PC += 3

    def run(self):
        """
        This method runs until there is no more instructions left 
        or the HLT instruction is called. 
        The instructions are called using a dictionary.
        """


        time_stamp = datetime.datetime.now()
        while self.PC <= len(self.ram):
            IR = self.ram[self.PC]

            # Time Interupts
            new_time_stamp = datetime.datetime.now()
            difference = new_time_stamp - time_stamp
            if difference.__getattribute__('seconds') >= 1:
            	pass


            self.branchtable[IR](self.ram[self.PC + 1], self.ram[self.PC + 2])