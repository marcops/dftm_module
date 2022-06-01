from myhdl import *
from definitions import *

#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    def is_double_encode(mem):
        return mem > 1

    def encode(d, type):
        if type == ECC_NONE:
            return intbv(int(d))[WORD_DOUBLE_SIZE_WITH_ECC:]
        if type == ECC_PARITY:
            v = intbv((d << DISTANCE_ECC_ONE_MODULE))[WORD_DOUBLE_SIZE_WITH_ECC:]
            v[0] = d[0]^d[1]^d[2]^d[3]^d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]^d[11]^d[12]^d[13]^d[14]^d[15]
            return v
 
        if type == ECC_HAMMING:
            p = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            p[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            p[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            p[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            p[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            p[4] = d[11]^d[12]^d[13]^d[14]^d[15]
            v = intbv((d << DISTANCE_ECC_ONE_MODULE))[WORD_DOUBLE_SIZE_WITH_ECC:]
            v[0] = p[0]
            v[1] = p[1]
            v[2] = p[2]
            v[3] = p[3]
            v[4] = p[4]
            return v

        if type == ECC_LPC_WITHOUT_PARITY:
            v = intbv(int(d))[WORD_DOUBLE_SIZE_WITH_ECC:]
            v[16] = (d[0]^d[1])^d[3]
            v[17] = (d[0]^d[2])^d[3]
            v[18] = (d[1]^d[2])^d[3]
            v[19] = (d[4]^d[5])^d[7]
            v[20] = (d[4]^d[6])^d[7]
            v[21] = (d[5]^d[6])^d[7]
            v[22] = (d[8]^d[9])^d[11]
            v[23] = (d[8]^d[10])^d[11]
            v[24] = (d[9]^d[10])^d[11]
            v[25] = (d[12]^d[13])^d[15]
            v[26] = (d[12]^d[14])^d[15]
            v[27] = (d[13]^d[14])^d[15]
            v[28] = (d[0]^d[4])^d[12]
            v[29] = (d[0]^d[8])^d[12]
            v[30] = (d[4]^d[8])^d[12]
            v[31] = (d[1]^d[5])^d[13]
            v[32] = (d[1]^d[9])^d[13]
            v[33] = (d[5]^d[9])^d[13]
            v[34] = (d[2]^d[6])^d[14]
            v[35] = (d[2]^d[10])^d[14]
            v[36] = (d[6]^d[10])^d[14]
            v[37] = (d[3]^d[7])^d[15]
            v[38] = (d[3]^d[11])^d[15]
            v[39] = (d[7]^d[11])^d[15]
            return v

        return intbv(int(d))[WORD_DOUBLE_SIZE_WITH_ECC:]

    def check(data, type):
        if type == ECC_NONE:
            return True

        #parity check
        if type == ECC_PARITY:
            #0+DISTANCE_ECC_ONE_MODULE
            x = data[5]^data[6]^data[7]^data[8]^data[9]^data[10]^data[11]^data[12]^data[13]^data[14]^data[15]^data[16]^data[17]^data[18]^data[19]^data[20]
            return data[0] == x

        if type == ECC_HAMMING:
            dh = data[WORD_DOUBLE_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
            p = intbv(bool(0))[DISTANCE_ECC_ONE_MODULE:]
            p[0] = dh[0]^dh[1]^dh[3]^dh[4]^dh[6]^dh[8]^dh[10]^dh[11]^dh[13]^dh[15]
            p[1] = dh[0]^dh[2]^dh[3]^dh[5]^dh[6]^dh[9]^dh[10]^dh[12]^dh[13]
            p[2] = dh[1]^dh[2]^dh[3]^dh[7]^dh[8]^dh[9]^dh[10]^dh[14]^dh[15]
            p[3] = dh[4]^dh[5]^dh[6]^dh[7]^dh[8]^dh[9]^dh[10]
            p[4] = dh[11]^dh[12]^dh[13]^dh[14]^dh[15]
            return data[DISTANCE_ECC_ONE_MODULE:] == p
        if type == ECC_LPC_WITHOUT_PARITY:
            #print(bin(data))
            d = data[WORD_SIZE:]
            #print(bin(d))
            if data[16] != (d[0]^d[1])^d[3]:
                return False
            if data[17] != (d[0]^d[2])^d[3]:
                return False
            if data[18] != (d[1]^d[2])^d[3]:
                return False
            if data[19] != (d[4]^d[5])^d[7]:
                return False
            if data[20] != (d[4]^d[6])^d[7]:
                return False
            if data[21] != (d[5]^d[6])^d[7]:
                return False
            if data[22] != (d[8]^d[9])^d[11]:
                return False
            if data[23] != (d[8]^d[10])^d[11]:
                return False
            if data[24] != (d[9]^d[10])^d[11]:
                return False
            if data[25] != (d[12]^d[13])^d[15]:
                return False
            if data[26] != (d[12]^d[14])^d[15]:
                return False
            if data[27] != (d[13]^d[14])^d[15]:
                return False
            if data[28] != (d[0]^d[4])^d[12]:
                return False
            if data[29] != (d[0]^d[8])^d[12]:
                return False
            if data[30] != (d[4]^d[8])^d[12]:
                return False
            if data[31] != (d[1]^d[5])^d[13]:
                return False
            if data[32] != (d[1]^d[9])^d[13]:
                return False
            if data[33] != (d[5]^d[9])^d[13]:
                return False
            if data[34] != (d[2]^d[6])^d[14]:
                return False
            if data[35] != (d[2]^d[10])^d[14]:
                return False
            if data[36] != (d[6]^d[10])^d[14]:
                return False
            if data[37] != (d[3]^d[7])^d[15]:
                return False
            if data[38] != (d[3]^d[11])^d[15]:
                return False
            if data[39] != (d[7]^d[11])^d[15]:
                return False
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
            return intbv(int(((data) ^ (1 << np)) >> DISTANCE_ECC_ONE_MODULE))[WORD_SIZE:]

        if type == ECC_LPC_WITHOUT_PARITY:
            d = data[WORD_SIZE:]
            
            sR02 = data[16] ^ ((d[0]^d[1])^d[3])
            sR01 = data[17] ^ ((d[0]^d[2])^d[3])
            sR00 = data[18] ^ ((d[1]^d[2])^d[3])
            sR12 = data[19] ^ ((d[4]^d[5])^d[7])
            sR11 = data[20] ^ ((d[4]^d[6])^d[7])
            sR10 = data[21] ^ ((d[5]^d[6])^d[7])
            sR22 = data[22] ^ ((d[8]^d[9])^d[11])
            sR21 = data[23] ^ ((d[8]^d[10])^d[11])
            sR20 = data[24] ^ ((d[9]^d[10])^d[11])
            sR32 = data[25] ^ ((d[12]^d[13])^d[15])
            sR31 = data[26] ^ ((d[12]^d[14])^d[15])
            sR30 = data[27] ^ ((d[13]^d[14])^d[15])

            sC02 = data[28] ^ ((d[0]^d[4])^d[12])
            sC01 = data[29] ^ ((d[0]^d[8])^d[12])
            sC00 = data[30] ^ ((d[4]^d[8])^d[12])
            sC12 = data[31] ^ ((d[1]^d[5])^d[13])
            sC11 = data[32] ^ ((d[1]^d[9])^d[13])
            sC10 = data[33] ^ ((d[5]^d[9])^d[13])
            sC22 = data[34] ^ ((d[2]^d[6])^d[14])
            sC21 = data[35] ^ ((d[2]^d[10])^d[14])
            sC20 = data[36] ^ ((d[6]^d[10])^d[14])
            sC32 = data[37] ^ ((d[3]^d[7])^d[15])
            sC31 = data[38] ^ ((d[3]^d[11])^d[15])
            sC30 = data[39] ^ ((d[7]^d[11])^d[15])

            sR0 = sR00 | sR01 | sR02
            sR1 = sR10 | sR11 | sR12
            sR2 = sR20 | sR21 | sR22
            sR3 = sR30 | sR31 | sR32

            sC0 = sC00 | sC01 | sC02
            sC1 = sC10 | sC11 | sC12
            sC2 = sC20 | sC21 | sC22
            sC3 = sC30 | sC31 | sC32

            if sR0 == 1 and sC0 == 1:
                d[0] = ~d[0]
            if sR0 == 0 and sC1 == 1:
                d[1] = ~d[1]
            if sR0 == 0 and sC2 == 1:
                d[2] = ~d[2]
            if sR0 == 0 and sC3 == 1:
                d[3] = ~d[3]
            if sR1 == 1 and sC0 == 1:
                d[4] = ~d[4]
            if sR1 == 1 and sC1 == 1:
                d[5] = ~d[5]
            if sR1 == 1 and sC2 == 1:
                d[6] = ~d[6]
            if sR1 == 1 and sC3 == 1:
                d[7] = ~d[7]
            if sR2 == 1 and sC0 == 1:
                d[8] = ~d[8]
            if sR2 == 1 and sC1 == 1:
                d[9] = ~d[9]
            if sR2 == 1 and sC2 == 1:
                d[10] = ~d[10]
            if sR2 == 1 and sC3 == 1:
                d[11] = ~d[11]
            if sR3 == 1 and sC0 == 1:
                d[12] = ~d[12]
            if sR3 == 1 and sC1 == 1:
                d[13] = ~d[13]
            if sR3 == 1 and sC2 == 1:
                d[14] = ~d[14]
            if sR3 == 1 and sC3 == 1:
                d[15] = ~d[15]
           
            return d
        return intbv(int(data))[WORD_SIZE:]