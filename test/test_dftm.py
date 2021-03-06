from utils import *
import sys

# DFTM TESTs
#
# tst = TEST
# number of BITFLIP (BF)
# configuration mode STATIC (CS) DYNAMIC (CD)
# ECC starting in NONE, PARITY, HAMMING or REED SOLOMON
#

def tst_0BF_CS_NONE(host_intf):
    @instance
    def test():
        yield write_ram(host_intf, 20, 23)
        yield read_ram(host_intf, 20)
        t_asset_hex("tst_0BF_CS_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
    return test

def tst_0BF_CS_NONE_ManyRead(host_intf):
    @instance
    def test():
        yield write_ram(host_intf, 20, 23)
        yield read_ram(host_intf, 20)
        yield read_ram(host_intf, 20)
        yield read_ram(host_intf, 20)
        yield read_ram(host_intf, 20)
        t_asset_hex("tst_0BF_CS_NONE_ManyRead " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
    return test

def tst_0BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 1)

        # starting mem access
        yield write_ram(host_intf, 20, 23)
        yield read_ram(host_intf, 20)        
        t_asset_hex("tst_0BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        
        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_0BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 1)
    return test

def tst_1BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 1)

        # starting mem access
        yield write_ram(host_intf, 120, 23)
        yield read_ram(host_intf, 120)        
        t_asset_hex("tst_1BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        
        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_1BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 3)
    return test


def tst_2BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 3)

        # starting mem access
        #parity
        yield write_ram(host_intf, 120, 23)
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_2BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        
        #not fixable
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_2BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 0x1f)

        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_2BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 5)
    return test


def tst_3BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 3)

        # starting mem access
        yield write_ram(host_intf, 120, 23)
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_3BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        #not fixable - Parity
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_3BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 0x1f)

        #fixable - hamming
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_3BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)

        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_3BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 7)
    return test

def tst_4BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 3)

        # starting mem access
        yield write_ram(host_intf, 120, 23)
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_4BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        #not fixable - Parity
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_4BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 0x1f)

        #fixable - hamming
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_4BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)


        #fixable - LPC
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_4BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)

        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_4BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 7)
    return test

def tst_5BF_CD_NONE(host_intf):
    @instance
    def test():
        yield delay(140)
        # configuration DFTM
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 3)

       # starting mem access
        yield write_ram(host_intf, 120, 23)
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)
        #not fixable - Parity
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 0x1f)

        #fixable - hamming
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)


        #fixable - LPC
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)


        #KEEP ON LPC - fixable 
        yield write_ram(host_intf, 120, 23)
        yield bit_flip(host_intf, 120, [8])
        yield read_ram(host_intf, 120)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_MEM_DEFAULT, host_intf.data_o, 23)

        #check
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("tst_5BF_CD_NONE " + ERR_DFTM_MEM_DEFAULT, host_intf.data_o, 7)
    return test


fname = sys.argv[1]
dispatcher = {
    'tst_0BF_CS_NONE': (tst_0BF_CS_NONE, False, 5000),
    'tst_0BF_CS_NONE_ManyRead': (tst_0BF_CS_NONE_ManyRead, False, 7000),
    'tst_0BF_CD_NONE': (tst_0BF_CD_NONE, False, 7000),
    'tst_1BF_CD_NONE': (tst_1BF_CD_NONE, True, 15000),
    'tst_2BF_CD_NONE': (tst_2BF_CD_NONE, False, 20000),
    'tst_3BF_CD_NONE': (tst_3BF_CD_NONE, False, 25000),
    'tst_4BF_CD_NONE': (tst_4BF_CD_NONE, False, 25000),
    'tst_5BF_CD_NONE': (tst_5BF_CD_NONE, False, 25000),
}
try:
    f,s,t = dispatcher[fname]
    print("-------------------------------")
    print(fname)
    print("-------------------------------")
    test_run_bench(signal=s, func=f, timesteps=t)
except Exception as e:
    print("FAIL - " + fname + " - " + str(e))   
    raise e