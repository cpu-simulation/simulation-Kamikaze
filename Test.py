import copy


class Register:  # register : [b_n-1, ..., b_0]
    def __init__(self, size):
        self.size = size
        self.register = [0 for _ in range(size)]

    def INR(self):
        carry = 1
        for _ in range(self.size, 0, -1):
            current_bit = (self.register[_] + carry) % 2
            carry = (self.register[_] + carry) // 2
            self.register[_] = current_bit

    def LD(self, bus_obj: list):
        for _ in range(self.size):
            self.register[_] = bus_obj[_]

    def CLR(self):
        for _ in self.size:
            self.register[_] = 0


class Bus:
    def __init__(self):
        self.bus = [0 for _ in range(16)]

    def load_bus(self, data_list: list):
        for _ in range(16):
            self.bus[_] = data_list[_]


class Memory:
    def __init__(self):
        self.memory = dict()

    def convert_AR_to_address_for_read(self, adressreg: Register):
        return 0

    def read(self, ar: Register):
        adress = Memory.convert_AR_to_address_for_read(self, ar)
        Bus.load_bus(bus, self.memory[adress])

    def write(self, ar: Register):
        adress = Memory.convert_AR_to_address_for_read(self, ar)
        self.memory[adress] = copy.deepcopy(bus.bus)


AC = Register(16)  # Accumulator
AR = Register(12)  # Address Register
PC = Register(12)  # Program Counter
DR = Register(16)  # Data Register
IR = Register(16)  # Instruction Register
TC = Register(16)  # Temporary Register
E = Register(1)  # Carry Flag
bus = Bus()
memory = Memory()


# ALU IS DEFINED HERE
def alu_AND(A1: Register, A2: Register):  # set AC as A1 and A2
    result = [a & b for a, b in zip(A1.register, A2.register)]
    AC.register = copy.deepcopy(result)


def alu_OR(A1: Register, A2: Register):  # set AC as A1 or A2
    result = [a | b for a, b in zip(A1.register, A2.register)]
    AC.register = copy.deepcopy(result)


def alu_XOR(A1: Register, A2: Register):  # set AC as A1 xor A2
    result = [a ^ b for a, b in zip(A1.register, A2.register)]
    AC.register = copy.deepcopy(result)


def alu_COMPLEMENT(A1: Register):  # return ~A
    result = [1 - d for d in A1.register]
    return result


def alu_ADD(A1: Register, A2: Register):  # return A1 + A2
    result = [0] * 16
    carry = 0
    for i in range(15, -1, -1):
        total = A1.register[i] + A2.register[i] + carry
        result[i] = total % 2
        carry = total // 2
    E.register = carry
    return result


def alu_SUBTRACT():  # AC = AC-DR
    DR.register = alu_COMPLEMENT(DR)
    DR.INR()
    result = alu_ADD(AC, DR)
    AC.register = copy.deepcopy(result)


# CONTROL UNIT IS DEFINED HERE
def find_instruction(instruction_list: list):  # used to decode instructions
    instruction_number = 0
    for i in range(4):
        instruction_number += instruction_list[3 - i] * (2 ** i)
    return instruction_number


def AND():
    pass


def ADD():
    pass


def LDA():
    pass


def STA():
    pass


def BUN():
    pass


def BSA():
    pass


def ISZ():
    pass


def CLA():
    pass


def CLE():
    pass


def CMA():
    pass


def CIR():
    pass


def CIL():
    pass


def INC():
    pass


def SPA():
    pass


def SNA():
    pass


def SZA():
    pass


def SZE():
    pass


def HLT():
    pass


def decode_and_execute():
    Instruction_bits = IR.register[0:4]
    if find_instruction(Instruction_bits) == 0:
        AND()
    elif find_instruction(Instruction_bits) == 1:
        ADD()
    elif find_instruction(Instruction_bits) == 2:
        LDA()
    elif find_instruction(Instruction_bits) == 3:
        STA()
    elif find_instruction(Instruction_bits) == 4:
        BUN()
    elif find_instruction(Instruction_bits) == 5:
        BSA()
    elif find_instruction(Instruction_bits) == 6:
        ISZ()
    elif find_instruction(Instruction_bits) == 7:
        pass
    elif find_instruction(Instruction_bits) == 8:
        AR.register = IR.register[4:16]
        AND()
    elif find_instruction(Instruction_bits) == 9:
        AR = IR.register[4:16]
        ADD()
    elif find_instruction(Instruction_bits) == 10:
        pass
    elif find_instruction(Instruction_bits) == 11:
        pass
    elif find_instruction(Instruction_bits) == 12:
        pass
    elif find_instruction(Instruction_bits) == 13:
        pass
    elif find_instruction(Instruction_bits) == 14:
        pass
    elif find_instruction(Instruction_bits) == 15:
        pass
