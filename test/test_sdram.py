import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

from myhdl import *
from clk_driver import clk_driver
from sd_intf import SdramIntf
from sdram import sdram
from  utils import *

def test_readwrite(clk, sd_intf):

    driver = sd_intf.get_driver()

    @instance
    def test():
       
        sd_intf.cke.next = 1
        yield sd_intf.nop(clk)
        yield delay(5000)
        yield sd_intf.load_mode(clk)

        for p in range(4):            
            yield sd_intf.nop(clk)
            yield sd_intf.activate(clk, 17, bank_id=p)
            yield sd_intf.nop(clk)
            yield delay(10000)
        #yield delay(10000)
        while True:
            address = get_random_address()
            data = get_random_data()

            print(address)
            bank_id = int(address/8192)
            address = address%8192
            #print(address)            
            #print(bank_id)
            yield sd_intf.nop(clk)
            yield sd_intf.write(clk, driver, address, data,bank_id=bank_id)
            yield sd_intf.nop(clk)
            yield delay(10)
            yield sd_intf.read(clk, address, bank_id)
            yield sd_intf.nop(clk)
            yield delay(4)
            t_asset_hex("test_readwrite ", sd_intf.dq, data)
            
            #print ("sd_intf dq = ", sd_intf.dq.val, " @ ", now())

    return test

clk = Signal(bool(0))

clk_driver_Inst = clk_driver(clk)
sd_intf_Inst = SdramIntf()
sdram_Inst = sdram(clk, sd_intf_Inst)
test_readWrite_Inst = test_readwrite(clk, sd_intf_Inst)

sim = Simulation(clk_driver_Inst, sdram_Inst, test_readWrite_Inst)
sim.run(125000)
