import sys
sys.path.insert(0, 'source')

from myhdl import *
#from clk_driver import clk_driver
from conversion.convert_sdram_cntl import *

def convert_memory_controller(hdl):
    clk_i = Signal(bool(0))
    #rst_i = ResetSignal(0, active=1, isasync=True)
    #clkDriver_Inst = clk_driver(clk_i)
    sd_intf_Inst = SdramIntf()
    host_intf_Inst = HostIntf()

    sdramCntli = sdram_cntl(clk_i, host_intf_Inst, sd_intf_Inst)
    sdramCntli.convert(hdl)

convert_memory_controller(hdl='VHDL')