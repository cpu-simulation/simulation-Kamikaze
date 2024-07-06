import copy

import Components
from Components import AC, AR, PC, DR, IR, TC, E, memory, bus, branch_happened, Halt


def mem_ref_ins_compile(ins, ad):
    ad_part = ad[2:]
    for i in range(3-len(ad_part)):
        ins += '0'
    ins += ad_part
    return hex(int(ins, 16))


class Core:
    def __init__(self) -> None:
        pass

    def memory_write(self, data: dict) -> None:
        address = data["address"]
        value = data["value"]
        binary_address = bin(int(address, 16))[2:].zfill(12)
        binary_value = bin(int(str(value), 16))[2:].zfill(16)
        AR.register = [int(bit) for bit in binary_address]
        bus.load_bus([int(bit) for bit in binary_value])
        memory.write()

    def memory_bulk_write(self, data: list[dict]) -> None:
        for entry in data:
            self.memory_write(entry)

    def memory_bulk_read(self) -> list[dict]:
        result = []
        for address, value in memory.memory.items():
            hex_value = hex(int("".join(map(str, value)), 2))
            result.append({"address": address, "value": hex_value})
        return result

    def memory_read(self, address) -> dict:
        hex_address = hex(int(address, 16))
        if hex_address in memory.memory:
            value = memory.memory[hex_address]
            hex_value = hex(int("".join(map(str, value)), 2))
            return {"address": hex_address, "value": hex_value}
        else:
            return {"address": hex_address, "value": None}

    def register_write(self, data: dict[str, str]) -> None:
        for reg, value in data.items():
            binary_value = bin(int(value, 16))[2:]
            if reg == "AC":
                AC.register = [int(bit) for bit in binary_value.zfill(16)]
            elif reg == "E":
                E.register = [int(bit) for bit in binary_value.zfill(1)]
            elif reg == "PC":
                PC.register = [int(bit) for bit in binary_value.zfill(12)]
            elif reg == "IR":
                IR.register = [int(bit) for bit in binary_value.zfill(16)]
            elif reg == "AR":
                AR.register = [int(bit) for bit in binary_value.zfill(12)]
            elif reg == "DR":
                DR.register = [int(bit) for bit in binary_value.zfill(16)]
            elif reg == "E":
                E.register = [int(bit) for bit in binary_value.zfill(1)]

    def register_read(self) -> dict[str, str]:
        return {
            "AC": hex(int("".join(map(str, AC.register)), 2)),
            "E": hex(int("".join(map(str, E.register)), 2)),
            "PC": hex(int("".join(map(str, PC.register)), 2)),
            "IR": hex(int("".join(map(str, IR.register)), 2)),
            "AR": hex(int("".join(map(str, AR.register)), 2)),
            "DR": hex(int("".join(map(str, DR.register)), 2)),
            "TC": hex(int("".join(map(str, TC.register)), 2)),
        }

    def compile(self, instructions: list[str]) -> None:

        memory_instructions_dict = {'AND': '0x0', 'ANDI': '0x8', 'ADD': '0x1', 'ADDI': '0x9',
                                    'LDA': '0x2', 'LDAI': '0xA', 'STA': '0x3', 'STAI': '0xB',
                                    'BUN': '0x4', 'BUNI': '0xC', 'BSA': '0x5', 'BSAI': '0xD',
                                    'ISZ': '0x6', 'ISZI': '0xE'}
        register_instruction_dict = {'CLA': '0x7800', 'CLE': '0x7400', 'CMA': '0x7200', 'CME': '0x7100',
                                     'CIR': '0x7080', 'CIL': '0x7040', 'INC': '0x7020', 'SPA': '0x7010',
                                     'SNA': '0x7008', 'SZA': '0x7004', 'SZE': '0x7002', 'HLT': '0x7001'}
        address_in_mem = 0
        for ins in instructions:
            compiling = ins.split()
            if len(compiling) == 1:  # Register reference instruction
                ins_to_go = {'address': hex(address_in_mem), 'value': register_instruction_dict[compiling[0]]}

            else:  # Memory reference instruction
                ins_hex = mem_ref_ins_compile(memory_instructions_dict[compiling[0]], compiling[1])
                ins_to_go = {'address': hex(address_in_mem), 'value': ins_hex}
            Core.memory_write(self, ins_to_go)
            address_in_mem += 1

    def execute_instruction(self) -> None:
        while not Halt:
            bus.load_bus(PC.register)
            AR.LD()  # Setting AR to current PC since memory can only read AR and bus
            Components.fetch_instruction()
            Components.decode_and_execute()
            if not branch_happened:
                PC.INR()  # Go to the next instruction if the last instruction wasn't a branch
