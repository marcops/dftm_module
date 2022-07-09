import sys
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

from sdram_v import *

def convert_memory(hdl):
    clk_i = Signal(bool(0))
    sd_intf_Inst = SdramIntf()

    sdrami = sdram_vhdl(clk_i, sd_intf_Inst)
    sdrami.convert(hdl)

convert_memory(hdl='VHDL')
#convert_memory(hdl='Verilog')
