from myhdl import *
from definitions import *

#ECC_ENCODE = {'NONE': 0, 'PARITY':1,'HAMMING':2,'REED_SOLOMON':3
#x = ENCODE.get(0)

class ecc():
    def is_double_encode(mem):
        return mem > 1

    def encode(d, current_ecc):
        if current_ecc == ECC_NONE:
            return intbv(int(d))[WORD_DOUBLE_SIZE_WITH_ECC:]
        if current_ecc == ECC_PARITY:
            v = intbv((d << DISTANCE_ECC_ONE_MODULE))[WORD_DOUBLE_SIZE_WITH_ECC:]
            v[0] = d[0]^d[1]^d[2]^d[3]^d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]^d[11]^d[12]^d[13]^d[14]^d[15]
            return v
 
        if current_ecc == ECC_HAMMING:
            p = intbv(0)[DISTANCE_ECC_ONE_MODULE:]
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

        if current_ecc == ECC_LPC_WITHOUT_PARITY:
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

    def check(data, current_ecc):
        if current_ecc == ECC_NONE:
            return True

        #parity check
        if current_ecc == ECC_PARITY:
            #0+DISTANCE_ECC_ONE_MODULE
            x = data[5]^data[6]^data[7]^data[8]^data[9]^data[10]^data[11]^data[12]^data[13]^data[14]^data[15]^data[16]^data[17]^data[18]^data[19]^data[20]
            return data[0] == x

        if current_ecc == ECC_HAMMING:
            dh = data[WORD_DOUBLE_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
            p = intbv(0)[DISTANCE_ECC_ONE_MODULE:]
            p[0] = dh[0]^dh[1]^dh[3]^dh[4]^dh[6]^dh[8]^dh[10]^dh[11]^dh[13]^dh[15]
            p[1] = dh[0]^dh[2]^dh[3]^dh[5]^dh[6]^dh[9]^dh[10]^dh[12]^dh[13]
            p[2] = dh[1]^dh[2]^dh[3]^dh[7]^dh[8]^dh[9]^dh[10]^dh[14]^dh[15]
            p[3] = dh[4]^dh[5]^dh[6]^dh[7]^dh[8]^dh[9]^dh[10]
            p[4] = dh[11]^dh[12]^dh[13]^dh[14]^dh[15]
            return data[DISTANCE_ECC_ONE_MODULE:] == p
        if current_ecc == ECC_LPC_WITHOUT_PARITY:
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
        
    def decode(data, current_ecc):
        if current_ecc == ECC_NONE:
            return intbv(data)[WORD_SIZE:]
        if current_ecc == ECC_PARITY:
            return intbv(data)[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
        if current_ecc == ECC_HAMMING:
            d = data[WORD_SIZE_WITH_ECC:DISTANCE_ECC_ONE_MODULE]
            pg = intbv(0)[DISTANCE_ECC_ONE_MODULE:]
            pg[0] = d[0]^d[1]^d[3]^d[4]^d[6]^d[8]^d[10]^d[11]^d[13]^d[15]
            pg[1] = d[0]^d[2]^d[3]^d[5]^d[6]^d[9]^d[10]^d[12]^d[13]
            pg[2] = d[1]^d[2]^d[3]^d[7]^d[8]^d[9]^d[10]^d[14]^d[15]
            pg[3] = d[4]^d[5]^d[6]^d[7]^d[8]^d[9]^d[10]
            pg[4] = d[11]^d[12]^d[13]^d[14]^d[15]
            p = pg^data[DISTANCE_ECC_ONE_MODULE:]

            """Terrible code but its fast"""
            if p == 0:
                return intbv(d)[WORD_SIZE:]
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
            #TODO AQUI
            va = 1 << np
            vb = data ^ va
            vc = vb >> DISTANCE_ECC_ONE_MODULE
            return intbv(vc)[WORD_SIZE:]
            #return intbv(1)[WORD_SIZE:]

        if current_ecc == ECC_LPC_WITHOUT_PARITY:
            d = data[WORD_SIZE:]
            sR0 = intbv(0)[3:]
            sR1 = intbv(0)[3:]
            sR2 = intbv(0)[3:]
            sR3 = intbv(0)[3:]
            sC0 = intbv(0)[3:]
            sC1 = intbv(0)[3:]
            sC2 = intbv(0)[3:]
            sC3 = intbv(0)[3:]

            sR = intbv(0)[4:]
            sC = intbv(0)[4:]

            sR0[2] = data[16] ^ ((d[0]^d[1])^d[3])
            sR0[1] = data[17] ^ ((d[0]^d[2])^d[3])
            sR0[0] = data[18] ^ ((d[1]^d[2])^d[3])
            sR1[2] = data[19] ^ ((d[4]^d[5])^d[7])
            sR1[1] = data[20] ^ ((d[4]^d[6])^d[7])
            sR1[0] = data[21] ^ ((d[5]^d[6])^d[7])
            sR2[2] = data[22] ^ ((d[8]^d[9])^d[11])
            sR2[1] = data[23] ^ ((d[8]^d[10])^d[11])
            sR2[0] = data[24] ^ ((d[9]^d[10])^d[11])
            sR3[2] = data[25] ^ ((d[12]^d[13])^d[15])
            sR3[1] = data[26] ^ ((d[12]^d[14])^d[15])
            sR3[0] = data[27] ^ ((d[13]^d[14])^d[15])

            sC0[2] = data[28] ^ ((d[0]^d[4])^d[12])
            sC0[1] = data[29] ^ ((d[0]^d[8])^d[12])
            sC0[0] = data[30] ^ ((d[4]^d[8])^d[12])
            sC1[2] = data[31] ^ ((d[1]^d[5])^d[13])
            sC1[1] = data[32] ^ ((d[1]^d[9])^d[13])
            sC1[0] = data[33] ^ ((d[5]^d[9])^d[13])
            sC2[2] = data[34] ^ ((d[2]^d[6])^d[14])
            sC2[1] = data[35] ^ ((d[2]^d[10])^d[14])
            sC2[0] = data[36] ^ ((d[6]^d[10])^d[14])
            sC3[2] = data[37] ^ ((d[3]^d[7])^d[15])
            sC3[1] = data[38] ^ ((d[3]^d[11])^d[15])
            sC3[0] = data[39] ^ ((d[7]^d[11])^d[15])

            sR[0] = sR0[2] | sR0[1] | sR0[0]
            sR[1] = sR1[2] | sR1[1] | sR1[0]
            sR[2] = sR2[2] | sR2[1] | sR2[0]
            sR[3] = sR3[2] | sR3[1] | sR3[0]

            sC[0] = sC0[2] | sC0[1] | sC0[0]
            sC[1] = sC1[2] | sC1[1] | sC1[0]
            sC[2] = sC2[2] | sC2[1] | sC2[0]
            sC[3] = sC3[2] | sC3[1] | sC3[0]

            if sR[0] == 1 and sC[0] == 1:
                d[0] = not d[0]
            if sR[0] == 0 and sC[1] == 1:
                d[1] = not d[1]
            if sR[0] == 0 and sC[2] == 1:
                d[2] = not d[2]
            if sR[0] == 0 and sC[3] == 1:
                d[3] = not d[3]
            if sR[1] == 1 and sC[0] == 1:
                d[4] = not d[4]
            if sR[1] == 1 and sC[1] == 1:
                d[5] = not d[5]
            if sR[1] == 1 and sC[2] == 1:
                d[6] = not d[6]
            if sR[1] == 1 and sC[3] == 1:
                d[7] = not d[7]
            if sR[2] == 1 and sC[0] == 1:
                d[8] = not d[8]
            if sR[2] == 1 and sC[1] == 1:
                d[9] = not d[9]
            if sR[2] == 1 and sC[2] == 1:
                d[10] = not d[10]
            if sR[2] == 1 and sC[3] == 1:
                d[11] = not d[11]
            if sR[3] == 1 and sC[0] == 1:
                d[12] = not d[12]
            if sR[3] == 1 and sC[1] == 1:
                d[13] = not d[13]
            if sR[3] == 1 and sC[2] == 1:
                d[14] = not d[14]
            if sR[3] == 1 and sC[3] == 1:
                d[15] = not d[15]           
            return d
        return intbv(data)[WORD_SIZE:]