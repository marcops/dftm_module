import random
from myhdl import *
from dftm import dftm

random.seed(5)
randrange = random.randrange

@block
def test_dftm():

    ecc_type = Signal(intbv(0)[2:])
    address = Signal(intbv(0)[16:])
    command = Signal(intbv(0))

    dftm_result = dftm(ecc_type, address, command)

    @instance
    def stimulus():
        print("ecc address")
        for i in range(3):
            #address.next = randrange(8)
            yield delay(10)
            print("%s %s" % (ecc_type, address))

    return dftm_result, stimulus

tb = test_dftm()
tb.run_sim()