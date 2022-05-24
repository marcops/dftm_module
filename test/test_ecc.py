from utils import *
import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/ecc')

def test_parity_encode():
    lst = [1,0,0,1,0,1,1,0]

    for i in range(7):
        ve = ecc.encode(i, ecc.PARITY)
        isOK = ecc.check(ve, ecc.PARITY)
        p = ve & 0x1
        vd = ecc.decode(ve, ecc.PARITY)
        
        t_asset_hex("test_parity_encode - check" , isOK, True)
        t_asset_hex("test_parity_encode - code/decode" , i, vd)
        t_asset_hex("test_parity_encode - parity" , lst[i], p)

def test_hamming_encode():
    v = 64211
    for i in range(0,21):

        r = ecc.encode(v, ecc.HAMMING)
        
        rs = (r ^ (1 << i))
        nr = ecc.decode(rs, ecc.HAMMING)

        # print("r: "+bin(r))
        # print("r2:"+bin(rs))
        # print("nr:"+ bin(nr))
        # print("")
        # print("or:"+bin(v))
        # print("co:"+ bin(nr>>5))
        t_asset_hex("test_hamming_encode - parity" , int(v), int(nr))

        #print(str(i) + ") "+ str(int(v) == int(nr)))


test_parity_encode()
test_hamming_encode()