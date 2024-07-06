import copy


class Register:  # Register : [b_n-1, ..., b_0]
    def __init__(self, size):
        self.size = size
        self.register = [0 for _ in range(size)]

    def INR(self):
        carry = 1
        for _ in range(self.size - 1, -1, -1):
            current_bit = (self.register[_] + carry) % 2
            carry = (self.register[_] + carry) // 2
            self.register[_] = current_bit

    def LD(self):
        global bus
        self.register = copy.deepcopy(bus.bus[16 - self.size:])

    def CLR(self):
        for _ in range(self.size):
            self.register[_] = 0


class Bus:
    def __init__(self):
        self.bus = [0 for _ in range(16)]

    def load_bus(self, data_list: list):
        bus.bus = [0] * 15  # reset the boss
        self.bus[16 - len(data_list):] = copy.deepcopy(data_list)


def convert_AR_to_address_for_read():
    global AR
    address = str()
    for i in AR.register:
        address += str(i)
    binary_address = int(address, 2)
    return str(hex(binary_address))


class Memory:
    def __init__(self):
        self.memory = dict()

    def read(self):
        address = convert_AR_to_address_for_read()
        bus.load_bus(self.memory[address])

    def write(self):
        address = convert_AR_to_address_for_read()
        self.memory[address] = copy.deepcopy(bus.bus)


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
def alu_AND(A1: Register, A2: Register):  # Set AC as A1 and A2
    result = [a & b for a, b in zip(A1.register, A2.register)]
    AC.register = copy.deepcopy(result)


def alu_OR():  # Set AC as AC or DR
    result = [a | b for a, b in zip(DR.register, AC.register)]
    AC.register = copy.deepcopy(result)


def alu_XOR(A1: Register, A2: Register):  # Set AC as AC xor DR
    result = [a ^ b for a, b in zip(A1.register, A2.register)]
    AC.register = copy.deepcopy(result)


def alu_COMPLEMENT(A1: Register):  # Return ~A
    result = [1 - d for d in A1.register]
    return result


def alu_ADD(A1: Register, A2: Register):  # Return A1 + A2
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
def find_memory_reference_instruction(instruction_list: list):  # Used to decode instructions
    inst = ''
    for i in instruction_list:
        inst += str(i)
    return int(inst, 2)


def find_register_reference_instruction():
    s = str()
    for i in AR.register:
        s += str(i)
    binary_num = int(s, 2)
    reg_ref_code = str(hex(binary_num))
    return reg_ref_code[2:]


branch_happened = False
Halt = False


# Memory reference instructions:
def AND():
    alu_AND(DR, AC)


def ADD():
    alu_ADD(DR, AC)


def LDA():
    memory.read()
    AC.LD()


def STA():
    bus.load_bus(AC.register)
    memory.write()


def BUN():
    global branch_happened
    branch_happened = True
    PC.register = copy.deepcopy(AR.register)


def BSA():
    global branch_happened
    branch_happened = True
    bus.load_bus(PC.register)
    memory.write()
    bus.load_bus(AR.register)
    PC.LD()
    PC.INR()


def ISZ():
    memory.read()
    DR.LD()
    DR.INR()
    if DR.register == [0 for i in range(16)]:
        PC.INR()


# Register reference instructions:
def CLA():
    AC.CLR()


def CLE():
    E.CLR()


def CMA():
    AC.register = copy.deepcopy(alu_COMPLEMENT(AC))


def CME():
    E.register = copy.deepcopy(alu_COMPLEMENT(E))


def CIR():
    E.register[0] = copy.deepcopy(AC.register[15])
    for i in range(15, 0, -1):
        AC.register[i] = copy.deepcopy(AC.register[i - 1])
    AC.register[0] = copy.deepcopy(E.register[0])


def CIL():
    E.register[0] = copy.deepcopy(AC.register[0])
    for i in range(15):
        AC.register[i] = copy.deepcopy(AC.register[i + 1])
    AC.register[15] = copy.deepcopy(E.register[0])


def INC():
    AC.INR()


def SPA():
    if AC.register[0] == 0:
        PC.INR()


def SNA():
    if AC.register[0] == 1:
        PC.INR()


def SZA():
    if AC.register == [0 for i in range(16)]:
        PC.INR()


def SZE():
    if E.register == [0]:
        PC.INR()


def HLT():
    global Halt
    Halt = True


memory_reference_instructions_dict = {
    0: AND, 1: ADD, 2: LDA, 3: STA,
    4: BUN, 5: BSA, 6: ISZ
}
register_reference_instruction_dict = {
    '800': CLA, '400': CLE, '200': CMA, '100': CME,
    '80': CIR, '40': CIL, '20': INC, '10': SPA,
    '8': SNA, '4': SZA, '2': SZE, '1': HLT
}


def fetch_instruction():
    global AR
    memory.read()
    IR.LD()


def decode_and_execute():
    global branch_happened
    global AR
    branch_happened = False
    Instruction_bits = IR.register[:4]
    AR.register = copy.deepcopy(IR.register[4:])
    op_code = find_memory_reference_instruction(Instruction_bits)

    if op_code < 7 and op_code != 3:  # Direct addressing
        memory.read()
        DR.LD()
        operation = memory_reference_instructions_dict[op_code]
        operation()

    elif op_code == 3:
        bus.load_bus(AC.register)
        memory.write()

    elif op_code == 7:  # Register reference
        reg_code = find_register_reference_instruction()
        register_op = register_reference_instruction_dict[reg_code]
        register_op()

    elif op_code < 11 or op_code == 14:  # Indirect addressing
        memory.read()
        AR.LD()  # Go to the effective address
        memory.read()
        DR.LD()
        operation = memory_reference_instructions_dict[op_code - 8]
        operation()

    else:
        memory.read()
        IR.LD()
        AR.register = copy.deepcopy(IR.register[4:])
        operation = memory_reference_instructions_dict[op_code - 8]
        operation()
