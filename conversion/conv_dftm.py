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
    sd_intf_Inst1 = SdramIntf()
    sd_intf_Inst2 = SdramIntf()
    ext_intf_Inst = ExtIntf()
    host_intf_sdram_Inst1 = HostIntf()
    host_intf_sdram_Inst2 = HostIntf()
   
    sdram_Inst1 = sdram(clk_i, sd_intf_Inst1, show_command=False)
    sdram_Inst2 = sdram(clk_i, sd_intf_Inst2, show_command=False)
    sdramCntl_Inst1 = sdram_cntl(clk_i, host_intf_sdram_Inst1, sd_intf_Inst1)
    sdramCntl_Inst2 = sdram_cntl(clk_i, host_intf_sdram_Inst2, sd_intf_Inst2)
    sdramCntli = dftm(clk_i, ext_intf_Inst, host_intf_sdram_Inst1, host_intf_sdram_Inst2)

    sdramCntli.convert(hdl)

convert_memory_controller(hdl='VHDL')
convert_memory_controller(hdl='Verilog')