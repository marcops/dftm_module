from myhdl import *


class dftm_ram():  
    def get_position(addr, page_size):
        return addr // page_size 
  
    def get_next_encode(enc):
        LAST_ENCODE = 3
        if enc >= 3:
            return enc
        else:
            return enc + 1

    def set_encode(mem, enc):
        mem.next[1] = enc[0]
        mem.next[2] = enc[1]
    def get_encode(mem):
        d = intbv(bool(0))[2:]
        d[0] = mem[1]
        d[1] = mem[2]
        return d

    def get_configuration(mem):
        return mem[0]
    def set_configuration(mem, config):
        mem.next[0] = config        
    
    
