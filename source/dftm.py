from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from ecc import *

from enum import Enum

@block
def dftm(clk_i, host_intf, host_intf_sdram):
    """INTERNAL RAM START"""
    IRAM_PAGE_SIZE = 256
    IRAM_DATA_SIZE = 3
    IRAM_ADDR_AMOUNT = 256
    ram = [Signal(intbv(0)[IRAM_DATA_SIZE:0]) for i in range(IRAM_ADDR_AMOUNT)]
    """INTERNAL RAM END"""
    
    OPERATION_MODE = enum('NORMAL','RECODING')
    current_operation_mode = Signal(OPERATION_MODE.NORMAL)
    
    """RECODE """
    RECODING_MODE = enum('READ', 'WAIT_READ', 'WRITE', 'WAIT_WRITE')

    recode_position = Signal(intbv(0)[24:]) 
    recode_count = Signal(intbv(0)[16:]) 
    current_recoding_mode = Signal(RECODING_MODE.READ)

    """END RECODE"""

    @always(clk_i.posedge)
    def main():        
        if current_operation_mode == OPERATION_MODE.NORMAL:
            iram_current_position = dftm_ram.get_position(host_intf.addr_i, IRAM_PAGE_SIZE)
            page_encode = ram[iram_current_position]

            host_intf_sdram.addr_i.next = host_intf.addr_i
            host_intf_sdram.data_i.next = ecc.encoder(host_intf.data_i, page_encode)
            host_intf_sdram.rd_i.next = host_intf.rd_i
            host_intf_sdram.wr_i.next = host_intf.wr_i

            if host_intf_sdram.done_o:
                host_intf.data_o.next = host_intf_sdram.data_o                
                decode_ok = ecc.decoder(host_intf.data_i, page_encode)
                """FAKE ERR WHEN 120 """
                decode_ok = not (host_intf.rd_i and host_intf.addr_i == 120)

                if decode_ok == False:
                    print("JOIN STATE FAKE")
                    current_operation_mode.next = OPERATION_MODE.RECODING
                    current_recoding_mode.next = RECODING_MODE.READ
                    recode_position.next = iram_current_position
                    recode_count.next = 0
                    host_intf.done_o.next = False
                    host_intf_sdram.rd_i.next = False
                    host_intf_sdram.wr_i.next = False
                else:
                    host_intf.done_o.next = host_intf_sdram.done_o
            else:
                host_intf.done_o.next = host_intf_sdram.done_o
                host_intf.data_o.next = host_intf_sdram.data_o
        else:
            print("RECODING " , recode_position)
            if current_recoding_mode == RECODING_MODE.READ:
                print(current_recoding_mode)
                current_recoding_mode.next = RECODING_MODE.WAIT_READ
            if current_recoding_mode == RECODING_MODE.WAIT_READ:
                print(current_recoding_mode)
                current_recoding_mode.next = RECODING_MODE.WRITE
            if current_recoding_mode == RECODING_MODE.WRITE:
                print(current_recoding_mode)
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE
            if current_recoding_mode == RECODING_MODE.WAIT_WRITE:
                print(current_recoding_mode)
                host_intf.done_o.next = True
                current_operation_mode.next = OPERATION_MODE.NORMAL


    return main