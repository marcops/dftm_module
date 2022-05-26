from utils import *
import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

def test_parity_encode():
    lst = [1,1,0,0,0,0,1,0]

    for i in range(7):
        ni = intbv(i,None,None, 16)
        ve = ecc.encode(ni, ECC_PARITY)
        isOK = ecc.check(ve, ECC_PARITY)
        p = ve[0]
        vd = ecc.decode(ve, ECC_PARITY)
        
        t_asset_hex(str(i) + ")test_parity_encode - check" , isOK, True)
        t_asset_hex(str(i) + ")test_parity_encode - code/decode" , ni, vd)
        t_asset_hex(str(i) + ")test_parity_encode - parity" , lst[i], p)

def test_hamming_encode():
    v = 64211
    vi = intbv(v,None,None, 16)
    for i in range(0,21):

        r = ecc.encode(vi, ECC_HAMMING)
        isOK = ecc.check(r, ECC_HAMMING)
        rs = (r ^ (1 << i))
        nOK = ecc.check(rs, ECC_HAMMING)
        nr = ecc.decode(rs, ECC_HAMMING)

        t_asset_hex("test_hamming_encode - nok" , nOK, False)
        t_asset_hex("test_hamming_encode - ok" , isOK, True)
        t_asset_hex("test_hamming_encode - same value" , int(vi), int(nr))

        #print(str(i) + ") "+ str(int(v) == int(nr)))


test_parity_encode()
test_hamming_encode()