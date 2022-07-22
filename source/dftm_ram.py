from myhdl import *
from definitions import *
class dftm_ram():  
    
    def get_position(addr, page_size):
        return addr // page_size 
  
    def get_previous_encode(enc):
        #FIRST_ENCODE = 0
        if enc <= 1:
            return 1
        else:
            return enc - 1

    def get_next_encode(enc):
        #LAST_ENCODE = 3
        if enc >= 3:
            return 3
        else:
            return enc + 1

  

    def set_count_error(pmem, count):
        mem = intbv(0)[IRAM_DATA_SIZE:0]
        csig = intbv(count)[5:]

        mem[0] = pmem[0]
        mem[1] = pmem[1]
        mem[2] = pmem[2]
        POS_COUNT_ERROR = INIT_COUNT
        mem[POS_COUNT_ERROR] = csig[0]
        mem[POS_COUNT_ERROR+1] = csig[1]
        mem[POS_COUNT_ERROR+2] = csig[2]
        mem[POS_COUNT_ERROR+3] = csig[3]
        mem[POS_COUNT_ERROR+4] = csig[4]

        return mem

    def get_count_error(mem):
        POS_COUNT_ERROR = 3
        d = intbv(0)[5:]
        d[0] = mem[POS_COUNT_ERROR]
        d[1] = mem[POS_COUNT_ERROR+1]
        d[2] = mem[POS_COUNT_ERROR+2]
        d[3] = mem[POS_COUNT_ERROR+3]
        d[4] = mem[POS_COUNT_ERROR+4]
        return d

    def set_encode(pmem, enc):
        mem = intbv(pmem)[IRAM_DATA_SIZE:0]
        POS_ENCODE = 1
        mem[POS_ENCODE] = enc[0]
        mem[POS_ENCODE+1] = enc[1]
        return mem

    def get_encode(mem):
        POS_ENCODE = 1
        d = intbv(0)[2:]
        d[0] = mem[POS_ENCODE]
        d[1] = mem[POS_ENCODE+1]
        return int(d)

    def get_configuration(mem):
        return mem[0]
    def set_configuration(mem, config):
        mem[0] = config        
    
    
