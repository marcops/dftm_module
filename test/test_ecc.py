from utils import *
import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

def test_none_encode():
    for i in range(7):
        ni = intbv(i,None,None, WORD_SIZE)
        ve = ecc.encode(ni, ECC_NONE)
        isOK = ecc.check(ve, ECC_NONE)
        vd = ecc.decode(ve, ECC_NONE)
        
        t_asset_hex(str(i) + ")test_none_encode - check" , isOK, True)
        t_asset_hex(str(i) + ")test_none_encode - code" , ve, ni)
        t_asset_hex(str(i) + ")test_none_encode - decode" , vd, ni)


def test_parity_encode():
    lst = [0,1,1,0,1,0,0]

    for i in range(7):
        ni = intbv(i,None,None, WORD_SIZE)
        ve = ecc.encode(ni, ECC_PARITY)
        isOK = ecc.check(ve, ECC_PARITY)
        p = ve[0]
        vd = ecc.decode(ve, ECC_PARITY)
        
        t_asset_hex(str(i) + ")test_parity_encode - check" , isOK, True)
        t_asset_hex(str(i) + ")test_parity_encode - code/decode" , ni, vd)
        t_asset_hex(str(i) + ")test_parity_encode - parity" , lst[i], p)

def test_hamming_encode():
    v = 64211
    vi = intbv(v,None,None, WORD_SIZE)
    for i in range(0,WORD_SIZE_WITH_ECC):

        r = ecc.encode(vi, ECC_HAMMING)
        isOK = ecc.check(r, ECC_HAMMING)
        rs = (r ^ (1 << i))
        nOK = ecc.check(rs, ECC_HAMMING)
        nr = ecc.decode(rs, ECC_HAMMING)

        t_asset_hex(str(i) + ")test_hamming_encode - nok" , nOK, False)
        t_asset_hex(str(i) + ")test_hamming_encode - ok" , isOK, True)
        t_asset_hex(str(i) + ")test_hamming_encode - same value" , int(vi), int(nr))

        #print(str(i) + ") "+ str(int(v) == int(nr)))

def test_LPC_encode():
    v = 64211
    vi = intbv(v,None,None, WORD_SIZE)
    for i in range(0,WORD_SIZE_WITH_ECC):
        
        r = ecc.encode(vi, ECC_LPC_WITHOUT_PARITY)
        #print(bin(r))
        isOK = ecc.check(r, ECC_LPC_WITHOUT_PARITY)
        rs = (r ^ (1 << i))
        nOK = ecc.check(rs, ECC_LPC_WITHOUT_PARITY)
        nr = ecc.decode(r, ECC_LPC_WITHOUT_PARITY)
       # print(hex(v), "-", r , " - ", nr , " - ", rs)
        t_asset_hex(str(i) + ")test_LPC_encode - nok" , nOK, False)
        t_asset_hex(str(i) + ")test_LPC_encode - ok" , isOK, True)
        t_asset_hex(str(i) + ")test_LPC_encode - same value" , int(vi), int(nr))

test_LPC_encode()
test_parity_encode()
test_hamming_encode()
test_none_encode()