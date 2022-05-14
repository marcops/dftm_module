from myhdl import *


class dftm_ram():  
    def get_position(addr, page_size):
        return addr // page_size
  
    def get_encode(mem):
        return mem>>1
    def get_configuration(mem):
        return mem & 0x1

    def set_configuration(mem, config):
        mem.next[0] = config        
    def set_encode(mem, enc):
        mem.next[1] = (enc & 0x1)
        mem.next[2] = (enc & 0x2) >> 1
    
