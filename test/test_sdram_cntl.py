import sys
import random
from utils import *
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *



def test_readwrite(host_intf):

    def get_random_address():
        return random.randint(0, 65534)
    def get_random_data():
        return random.randint(0, 65534)

    @instance
    def test():
        while True:
            address = get_random_address()
            data = get_random_data()
            #yield delay(140)    
            yield write_ram(host_intf, address, data)        
            
            yield read_ram(host_intf, address)
            #yield delay(100)
            t_asset_hex("test_readwrite ", host_intf.data_o, data)
           
    return test

clk_i = Signal(bool(0))
#rst_i = ResetSignal(0, active=1, isasync=True)

clkDriver_Inst = clk_driver(clk_i)
sd_intf_Inst = SdramIntf()
host_intf_Inst = HostIntf()

sdram_Inst = sdram(clk_i, sd_intf_Inst, show_command=False)
sdramCntl_Inst = sdram_cntl(clk_i, host_intf_Inst, sd_intf_Inst)
# sdramCntl_Inst = traceSignals(MySdramCntl,host_intf_Inst,sd_intf_Inst)

test_readWrite_Inst = test_readwrite(host_intf_Inst)

sim = Simulation(clkDriver_Inst, sdram_Inst, sdramCntl_Inst, test_readWrite_Inst)
sim.run(100000)
