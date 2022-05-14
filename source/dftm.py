from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from decoder import *


@block
def dftm(clk_i, host_intf, host_intf_sdram):

    OP_MODE = enum('NORMAL','RECODING')
    current_operation = Signal(OP_MODE.NORMAL)

    @always(clk_i.posedge)
    def main():
        if current_operation == OP_MODE.NORMAL:
            host_intf_sdram.addr_i.next = host_intf.addr_i
            host_intf_sdram.data_i.next = host_intf.data_i
            host_intf_sdram.rd_i.next = host_intf.rd_i
            host_intf_sdram.wr_i.next = host_intf.wr_i

            if host_intf_sdram.done_o:
                host_intf.data_o.next = host_intf_sdram.data_o                
                status = decoder.check(host_intf.data_i, 0)
                """FAKE ERR WHEN 120 """
                status = host_intf.rd_i and host_intf.addr_i == 120
                if status:
                    current_operation.next = OP_MODE.RECODING
                else:
                    host_intf.done_o.next = host_intf_sdram.done_o
            else:
                host_intf.done_o.next = host_intf_sdram.done_o
                host_intf.data_o.next = host_intf_sdram.data_o
        else:
            print("RECODING")
            host_intf.done_o.next = True
            current_operation.next = OP_MODE.NORMAL


    return main