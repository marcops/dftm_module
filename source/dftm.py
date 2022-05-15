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
    IRAM_PAGE_SIZE = 1
    IRAM_DATA_SIZE = 3
    IRAM_ADDR_AMOUNT = 256
    ram = [Signal(intbv(0)[IRAM_DATA_SIZE:0]) for i in range(IRAM_ADDR_AMOUNT)]
    """INTERNAL RAM END"""
    
    OPERATION_MODE = enum('NORMAL','RECODING_UP', 'RECODING_DOWN')
    current_operation_mode = Signal(OPERATION_MODE.NORMAL)
    
    """RECODE """
    RECODING_MODE = enum('READ', 'WAIT_READ', 'WRITE', 'WAIT_WRITE')

    recode_position = Signal(intbv(0)[24:]) 
    recode_count = Signal(intbv(0)[16:]) 
    recode_data_o = Signal(intbv(0)[16:])
    recode_current_ecc = Signal(intbv(0)[IRAM_DATA_SIZE:])
    current_recoding_mode = Signal(RECODING_MODE.READ)
    """END RECODE"""

    @always(clk_i.posedge)
    def main():        
        if current_operation_mode == OPERATION_MODE.NORMAL:
            iram_current_position = dftm_ram.get_position(host_intf.addr_i, IRAM_PAGE_SIZE)
            ram_inf = ram[iram_current_position]
            current_encode = dftm_ram.get_encode(ram_inf)

            host_intf_sdram.addr_i.next = host_intf.addr_i
            host_intf_sdram.data_i.next = ecc.encoder(host_intf.data_i, current_encode)
            host_intf_sdram.rd_i.next = host_intf.rd_i
            host_intf_sdram.wr_i.next = host_intf.wr_i

            if host_intf_sdram.done_o:
                host_intf.data_o.next = host_intf_sdram.data_o                
                decode_ok = ecc.decoder_check(host_intf.data_i, current_encode)
                """FAKE ERR WHEN 120 """
                decode_ok = not (host_intf.rd_i and host_intf.addr_i == 120)
                
                if decode_ok == False:
                    print("JOIN STATE FAKE")
                    recode = dftm_ram.get_next_encode(current_encode) != current_encode
                    if recode:
                        current_operation_mode.next = OPERATION_MODE.RECODING_UP
                        current_recoding_mode.next = RECODING_MODE.READ
                        recode_position.next = iram_current_position
                        recode_current_ecc.next = current_encode
                        recode_count.next = 0
                        host_intf.done_o.next = False
                        host_intf_sdram.rd_i.next = False
                        host_intf_sdram.wr_i.next = False
                    else:
                        host_intf.done_o.next = ecc.decoder(host_intf_sdram.done_o, current_encode)
                else:
                    host_intf.done_o.next = ecc.decoder(host_intf_sdram.done_o, current_encode)

            else:
                host_intf.done_o.next = ecc.decoder(host_intf_sdram.done_o, current_encode)
                host_intf.data_o.next = host_intf_sdram.data_o
                
        else:
            recoding_current_address =  (recode_position * IRAM_PAGE_SIZE) + recode_count
            print("RECODING " , recode_position, " - ", recode_count, " - ", recoding_current_address)

            if current_recoding_mode == RECODING_MODE.READ:
                print(current_recoding_mode)
                host_intf_sdram.addr_i.next = recoding_current_address
                host_intf_sdram.rd_i.next = 1
                current_recoding_mode.next = RECODING_MODE.WAIT_READ

            if current_recoding_mode == RECODING_MODE.WAIT_READ:
                print(current_recoding_mode)
                host_intf_sdram.rd_i.next = 0
                if host_intf_sdram.done_o:
                    current_recoding_mode.next = RECODING_MODE.WRITE
                    recode_data_o.next = ecc.decoder(host_intf_sdram.data_o, recode_current_ecc)
                    """TODO IGNORING THE DECODE ERROR """
                    print("RECODING READ ", host_intf_sdram.data_o)

            if current_recoding_mode == RECODING_MODE.WRITE:
                print(current_recoding_mode)
                host_intf_sdram.addr_i.next = recoding_current_address
                host_intf_sdram.data_i.next = ecc.encoder(recode_data_o, dftm_ram.get_next_encode(recode_current_ecc))
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE

            if current_recoding_mode == RECODING_MODE.WAIT_WRITE:
                print(current_recoding_mode)
                host_intf_sdram.wr_i.next = 1

                if host_intf_sdram.done_o:
                    host_intf_sdram.rd_i.next = 0
                    host_intf_sdram.wr_i.next = 0
                    r_count =  recode_count +1
                    if r_count < IRAM_PAGE_SIZE:
                        current_recoding_mode.next = RECODING_MODE.READ
                        recode_count.next = r_count
                    else:
                        """RECODING DONE"""
                        host_intf.done_o.next = True
                        current_operation_mode.next = OPERATION_MODE.NORMAL
                    

    return main