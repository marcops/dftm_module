from myhdl import *
from definitions import *

#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    def encode(data, type):
        if type == ECC_NONE:
            return intbv(int(data))[BIT_SIZE_ONE_MODULE:]
        if type == ECC_PARITY:
            x = False
            x ^= data[8]
            x ^= data[4]
            x ^= data[2]
            x ^= data[1]
            x = (~x) & 1
            v = intbv((data << DISTANCE_ECC_ONE_MODULE))[BIT_SIZE_ONE_MODULE:]
            v[0] = x
            return v
 
        if type == ECC_HAMMING:
            d = data
            p0 = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p1 = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p2 = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p3 = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p4 = d[11]^d[12]^d[13]^d[14]^d[15]
            v = intbv((data << DISTANCE_ECC_ONE_MODULE))[BIT_SIZE_ONE_MODULE:]
            v[0] = p0
            v[1] = p1
            v[2] = p2
            v[3] = p3
            v[4] = p4
            return v

        if type == ECC_REED_SOLOMON:
            return intbv(int(data))[BIT_SIZE_ONE_MODULE:]
        return intbv(int(data))[BIT_SIZE_ONE_MODULE:]

    def check(data, type):
        if type == ECC_NONE:
            return True

        #parity check
        if type == ECC_PARITY:
            c = data[0]
            x = False
            x ^= data[8+ DISTANCE_ECC_ONE_MODULE]
            x ^= data[4+ DISTANCE_ECC_ONE_MODULE]
            x ^= data[2+ DISTANCE_ECC_ONE_MODULE]
            x ^= data[1+ DISTANCE_ECC_ONE_MODULE]
            x = (~x) & 1
            return c == x

        if type == ECC_HAMMING:
            d = data[BIT_SIZE_ONE_MODULE:5]
            p = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            p[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p[5] = d[11]^d[12]^d[13]^d[14]^d[15]
            check = data[:DISTANCE_ECC_ONE_MODULE]
            return check == p
        if type == ECC_REED_SOLOMON:
            return True
        return False
        
    def decode(data, type):
        if type == ECC_NONE:
            return intbv(int(data))[BIT_SIZE_IN:]
        if type == ECC_PARITY:
            return intbv(int(data >> DISTANCE_ECC_ONE_MODULE))[BIT_SIZE_IN:]
        if type == ECC_HAMMING:
            d = data >> DISTANCE_ECC_ONE_MODULE
            p0 = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p1 = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p2 = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p3 = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p4 = d[11]^d[12]^d[13]^d[14]^d[15]
            pg = ((p4<<4)|(p3<<3)|(p2<<2)|(p1<<1)|p0)
            pr = data & 31

            p = pg^pr
            if p == 0:
                return intbv(int(d))[BIT_SIZE_IN:]
            np =0
            if p == 1:
                np = 0
            if p == 2 :
                np = 1
            if p==17:
                np = 16
            if p==18:
                np = 17
            if p==19:
                np = 18
            if p==20:
                np = 19
            if p==21:
                np = 20
            if p==22:
                np = 21
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
            #data[np] = not data[np]

            return intbv(int(((data) ^ (1 << np)) >> DISTANCE_ECC_ONE_MODULE))[BIT_SIZE_IN:]
            #return intbv(int((data) >> 5))[BIT_SIZE_IN:]
        if type == ECC_REED_SOLOMON:
            return intbv(int(data))[BIT_SIZE_IN:]
        return intbv(int(data))[BIT_SIZE_IN:]