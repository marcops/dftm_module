from myhdl import *
from definitions import *

#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    def encode(d, type):
        if type == ECC_NONE:
            return intbv(int(d))[WORD_SIZE_WITH_ECC:]
        if type == ECC_PARITY:
            v = intbv((d << DISTANCE_ECC_ONE_MODULE))[WORD_SIZE_WITH_ECC:]
            v[0] = d[0]^d[1]^d[2]^d[3]^d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]^d[11]^d[12]^d[13]^d[14]^d[15]
            return v
 
        if type == ECC_HAMMING:
            p = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            p[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p[4] = d[11]^d[12]^d[13]^d[14]^d[15]
            v = intbv((d << DISTANCE_ECC_ONE_MODULE))[WORD_SIZE_WITH_ECC:]
            v[0] = p[0]
            v[1] = p[1]
            v[2] = p[2]
            v[3] = p[3]
            v[4] = p[4]
            return v

        if type == ECC_REED_SOLOMON:
            return intbv(int(d))[WORD_SIZE_WITH_ECC:]
        return intbv(int(d))[WORD_SIZE_WITH_ECC:]

    def check(data, type):
        if type == ECC_NONE:
            return True

        #parity check
        if type == ECC_PARITY:
            #0+DISTANCE_ECC_ONE_MODULE
            x = data[5]^data[6]^data[7]^data[8]^data[9]^data[10]^data[11]^data[12]^data[13]^data[14]^data[15]^data[16]^data[17]^data[18]^data[19]^data[20]
            return data[0] == x

        if type == ECC_HAMMING:
            d = data[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
            p = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            p[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p[4] = d[11]^d[12]^d[13]^d[14]^d[15]
            return data[DISTANCE_ECC_ONE_MODULE:] == p
        if type == ECC_REED_SOLOMON:
            return True
        return False
        
    def decode(data, type):
        if type == ECC_NONE:
            return intbv(int(data))[WORD_SIZE:]
        if type == ECC_PARITY:
            return intbv(int(data))[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
        if type == ECC_HAMMING:
            d = data[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
            pg = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            pg[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            pg[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            pg[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            pg[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            pg[4] = d[11]^d[12]^d[13]^d[14]^d[15]
            p = pg^data[DISTANCE_ECC_ONE_MODULE:]

            """Terrible code but its fast"""
            if p == 0:
                return intbv(int(d))[WORD_SIZE:]
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
            """end terrible code"""
            #ndata = data
            #data[np] = not data[np]
            #return data
            return intbv(int(((data) ^ (1 << np)) >> DISTANCE_ECC_ONE_MODULE))[WORD_SIZE:]
            #return ndata[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]

        if type == ECC_REED_SOLOMON:
            return intbv(int(data))[WORD_SIZE:]
        return intbv(int(data))[WORD_SIZE:]