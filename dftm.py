from myhdl import *

@block
def dftm(curr_ecc, address, command):
    #PAGE_SIZE - shoud be dynamic 
    PAGE_SIZE = 256
    MEMORY_SIZE = 256
    COMMAND_WRITE = 1
    
    #memory_0, memory_1, memory_2 = [[Signal(intbv(0))*MEMORY_SIZE] for i in range(3)]
    memory_1 = Signal(intbv(0)[MEMORY_SIZE:0])
    memory_2 = Signal(intbv(0)[MEMORY_SIZE:0])
    #memory_0, memory_1, memory_2 = [[] for i in range(3)]

    #ECC_TYPE = enum(
    #    'NONE',
    #    'PARITY',
    #    'HAMMING',
    #    'REED'
    #)

    #def get_ecc_name(ecc_int):
    #    return {
    #        0: Signal(ECC_TYPE.NONE),
    #        1: Signal(ECC_TYPE.PARITY),
    #        2: Signal(ECC_TYPE.HAMMING),
    #        3: Signal(ECC_TYPE.REED)
    #    }[ecc_int]

    def discover_current_ecc(address):
        position = address // PAGE_SIZE
        return memory_1[position] + (memory_2[position] << 1)

    @always_comb
    def process():
        curr_ecc.next = discover_current_ecc(address)
        if command == COMMAND_WRITE:
            return process

    return process