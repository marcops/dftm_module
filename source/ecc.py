from myhdl import *
from host_intf import *
#from parity import *
#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    def encoder(data, type):
        if type == 0:
            return data
        if type == 1:
            return data
        #    return Parity.encode(int(data))
        if type == 2:
            return data
        if type == 3:
            return data
        return data

    def decoder_check(data, type):
        if type == 0:
            return True
        if type == 1:
            return True
        #    return Parity.check(int(data))
        if type == 2:
            return True
        if type == 3:
            return True
        return False
        
    def decoder(data, type):
        if type == 0:
            return data
        if type == 1:
        #    return Parity.decode(int(data))
            return data
        if type == 2:
            return data
        if type == 3:
            return data
        return data