import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

from myhdl import *
#from clk_driver import clk_driver
from dftm import *
from sdram_cntl import *
def convert_memory_controller(hdl):
    clk_i = Signal(bool(0))
    #rst_i = ResetSignal(0, active=1, isasync=True)
    #clkDriver_Inst = clk_driver(clk_i)
    sd_intf_Inst = SdramIntf()
    ext_intf_Inst = ExtIntf()
    host_intf_sdram_Inst = HostIntf()
   
    sdram_Inst = sdram(clk_i, sd_intf_Inst, show_command=False)
    sdramCntl_Inst = sdram_cntl(clk_i, host_intf_sdram_Inst, sd_intf_Inst)
    sdramCntli = dftm(clk_i, ext_intf_Inst, host_intf_sdram_Inst)
    sdramCntli.convert(hdl)

convert_memory_controller(hdl='VHDL')
convert_memory_controller(hdl='Verilog')