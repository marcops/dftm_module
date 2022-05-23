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
            d = data
            p0 = (d&1)^(d>>1&1)^(d>>3&1)^(d>>4&1)^(d>>6&1)^(d>>8&1)^(d>>10&1)^(d>>11&1)^(d>>13&1)^(d>>15&1)
            p1 = (d&1)^(d>>2&1)^(d>>3&1)^(d>>5&1)^(d>>6&1)^(d>>9&1)^(d>>10&1)^(d>>12&1)^(d>>13&1)
            p2 = (d>>1&1)^(d>>2&1)^(d>>3&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)^(d>>14&1)^(d>>15&1)
            p3 = (d>>4&1)^(d>>5&1)^(d>>6&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)
            p4 = (d>>11&1)^(d>>12&1)^(d>>13&1)^(d>>14&1)^(d>>15&1)
            return (d << 5)|(p4<<4)|(p3<<3)|(p2<<2)|(p1<<1)|p0

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
            d = data >> 5
            p0 = (d&1)^(d>>1&1)^(d>>3&1)^(d>>4&1)^(d>>6&1)^(d>>8&1)^(d>>10&1)^(d>>11&1)^(d>>13&1)^(d>>15&1)
            p1 = (d&1)^(d>>2&1)^(d>>3&1)^(d>>5&1)^(d>>6&1)^(d>>9&1)^(d>>10&1)^(d>>12&1)^(d>>13&1)
            p2 = (d>>1&1)^(d>>2&1)^(d>>3&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)^(d>>14&1)^(d>>15&1)
            p3 = (d>>4&1)^(d>>5&1)^(d>>6&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)
            p4 = (d>>11&1)^(d>>12&1)^(d>>13&1)^(d>>14&1)^(d>>15&1)
            check = data & 31
            return check == ((p4<<4)|(p3<<3)|(p2<<2)|(p1<<1)|p0)
        if type == 3:
            return True
        return False
        
    def decode(data, type):
        if type == 0:
            return data
        if type == 1:
            return data >> 1
        if type == 2:
            d = data >> 5
            p0 = (d&1)^(d>>1&1)^(d>>3&1)^(d>>4&1)^(d>>6&1)^(d>>8&1)^(d>>10&1)^(d>>11&1)^(d>>13&1)^(d>>15&1)
            p1 = (d&1)^(d>>2&1)^(d>>3&1)^(d>>5&1)^(d>>6&1)^(d>>9&1)^(d>>10&1)^(d>>12&1)^(d>>13&1)
            p2 = (d>>1&1)^(d>>2&1)^(d>>3&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)^(d>>14&1)^(d>>15&1)
            p3 = (d>>4&1)^(d>>5&1)^(d>>6&1)^(d>>7&1)^(d>>8&1)^(d>>9&1)^(d>>10&1)
            p4 = (d>>11&1)^(d>>12&1)^(d>>13&1)^(d>>14&1)^(d>>15&1)
            pg = ((p4<<4)|(p3<<3)|(p2<<2)|(p1<<1)|p0)
            pr = data & 31

            p = pg^pr
            if p == 0:
                return d
            np =0
            if p == 1 or p == 2 or p>=17:
                np = p-1
            if p == 4:
                np = 2
            if p == 8:
                np = 3
            if p == 16:
                np = 4
            if p == 3:
                np = 5
            if p >= 5 and p < 9 and p != 8:
                np = p+1
            if p>=9 and p <=15:
                np = p

            return (data ^ (1 << np)) >> 5
        if type == 3:
            return data
        return data