from myhdl import *


class dftm_ram():  
    def get_position(addr, page_size):
        return addr // page_size
  
    def get_next_encode(enc):
        LAST_ENCODE = 3
        if enc >= 3:
            #print("more:",enc)
            return enc
        else:
            #print("enc+1:",enc)
            return enc + 1
    def get_encode(mem):
        return mem>>1
    def get_configuration(mem):
        return mem & 0x1

    def set_configuration(mem, config):
        mem.next[0] = config        
    def set_encode(mem, enc):
        mem.next[1] = (enc & 0x1)
        mem.next[2] = (enc & 0x2) >> 1
    
