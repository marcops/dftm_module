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

test_parity_encode()




# v = 64211
# for i in range(0,21):

#     r = hamming_encode(v)
    
#     rs = (r ^ (1 << i))
#     nr = hamming_decode(rs)

#     print("r: "+bin(r))
#     print("r2:"+bin(rs))
#     print("nr:"+ bin(nr))
#     print("")
#     print("or:"+bin(v))
#     print("co:"+ bin(nr>>5))
#     100101100100101101011
#     10010110010010110101110000

#     print(str(i) + ") "+ str(int(v) == int(nr)))


