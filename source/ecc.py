from myhdl import *
from host_intf import *

#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    NONE = 0
    PARITY = 1
    HAMMING = 2
    REED_SOLOMON = 3
    
    def encode(data, type):
        if type == 0:
            return data
        if type == 1:
            x = data
            x ^= x >> 8
            x ^= x >> 4
            x ^= x >> 2
            x ^= x >> 1
            x = (~x) & 1
            return (data << 1) + x

        if type == 2:
            return data
        if type == 3:
            return data
        return data

    def check(data, type):
        if type == 0:
            return True

        #parity check
        if type == 1:
            c = data & 0x1	            
            x = data >> 1
            x ^= x >> 8
            x ^= x >> 4
            x ^= x >> 2
            x ^= x >> 1
            x = (~x) & 1
            return c == x

        if type == 2:
            return True
        if type == 3:
            return True
        return False
        
    def decode(data, type):
        if type == 0:
            return data
        if type == 1:
            return data >> 1
        if type == 2:
            return data
        if type == 3:
            return data
        return data