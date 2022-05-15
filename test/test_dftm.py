import sys

from myhdl import *
sys.path.insert(0, 'source')

from clk_driver import clk_driver
from sdram import *
from test.test_sdram_cntl import *
from test.test_dftm import *

def bench():
    #Signals
    clk_i = Signal(bool(0))
    sd_intf_Inst = SdramIntf()
    host_intf_Inst = HostIntf()
    host_intf_sdram_Inst = HostIntf()

    #Modules
    clkDriver_Inst = clk_driver(clk_i)
    sdram_Inst = sdram(clk_i, sd_intf_Inst, show_command=False)
    sdramCntl_Inst = sdram_cntl(clk_i, host_intf_sdram_Inst, sd_intf_Inst)
    dftm_Inst = dftm(clk_i, host_intf_Inst, host_intf_sdram_Inst)


    def write(addr,data):
        yield host_intf_Inst.write(addr, data)
        yield host_intf_Inst.done_o.posedge
        yield host_intf_Inst.nop()
        yield delay(3)
        print("[CPU-WRITE] addr: " , hex(addr) , ", data: ", hex(data))

    def read(addr):
        yield host_intf_Inst.read(addr)
        yield host_intf_Inst.done_o.posedge
        yield delay(1)
        print("[CPU-READ] addr: " , hex(addr) , ", data: ", hex(host_intf_Inst.data_o))
        
    @instance
    def test():
        yield delay(140)    
        yield write(120, 23)      
        yield read(120)     
        yield read(5)     
        yield write(5, 3)    
        yield read(5)
        yield read(1)
            
    return dftm_Inst , sdramCntl_Inst, sdram_Inst, clkDriver_Inst , test

def test_bench():
    b = bench()
    tb = traceSignals(bench)
    #b.config_sim(trace=True)
    sim =  Simulation(tb)
    #sim = Simulation(trace)
    sim.run(5000)

test_bench()
