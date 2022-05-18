from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from ecc import *

from enum import Enum

@block
def dftm(clk_i, host_intf, host_intf_sdram, dftm_iram_page_size = 1):
    OPERATION_MODE = enum('NORMAL','RECODING_UP', 'RECODING_DOWN')
    current_operation_mode = Signal(OPERATION_MODE.NORMAL)
    
    """INTERNAL RAM START"""
    IRAM_DATA_SIZE = 3
    IRAM_ADDR_AMOUNT = 128 # * 1000 #96kb
    ram = [Signal(intbv(0)[IRAM_DATA_SIZE:0]) for i in range(IRAM_ADDR_AMOUNT)]
    """INTERNAL RAM END"""
    
    """RECODE """
    RECODING_MODE = enum('READ', 'WAIT_READ', 'WRITE', 'WAIT_WRITE', 'WAIT_WRITE_1', 'WAIT_WRITE_2')
    recode_position = Signal(intbv(0)[24:]) 
    recode_count = Signal(intbv(0)[16:]) 
    recode_data_o = Signal(intbv(0)[16:])
    recode_from_ecc = Signal(intbv(0)[IRAM_DATA_SIZE:])
    recode_to_ecc = Signal(intbv(0)[IRAM_DATA_SIZE:])
    current_recoding_mode = Signal(RECODING_MODE.READ)
    """END RECODE"""

    @always(clk_i.posedge)
    def main():        
        if current_operation_mode == OPERATION_MODE.NORMAL:
            iram_current_position = dftm_ram.get_position(host_intf.addr_i, dftm_iram_page_size)
            current_encode = 0
            """Accessing a area major than managed, we will read without encode"""
            if iram_current_position > 1:
                ram_inf = ram[iram_current_position-1]
                current_encode = dftm_ram.get_encode(ram_inf)
            #print("CUR-ENCODE", host_intf.addr_i, "-",current_encode)
            host_intf_sdram.addr_i.next = host_intf.addr_i            
            host_intf_sdram.rd_i.next = host_intf.rd_i
            host_intf_sdram.wr_i.next = host_intf.wr_i

            if host_intf_sdram.done_o:
                host_intf.data_o.next = host_intf_sdram.data_o                
                decode_ok = ecc.decoder_check(host_intf.data_i, current_encode)
                """TODO Test Propose only - BITFLIP WHEN 120 """
                decode_ok = not (host_intf.rd_i and host_intf.addr_i == 120)
                print("[DFTM] addr:", host_intf.data_i, ", ecc:", current_encode )
                if decode_ok == 0:
                    next_encode = dftm_ram.get_next_encode(current_encode)
                    recode = next_encode != current_encode
                    print("will recode:", recode)
                    if recode:
                        current_operation_mode.next = OPERATION_MODE.RECODING_UP
                        current_recoding_mode.next = RECODING_MODE.READ
                        recode_position.next = iram_current_position
                        recode_from_ecc.next = current_encode
                        recode_to_ecc.next = next_encode
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
            if recode_count == 0 and current_recoding_mode == RECODING_MODE.READ:
                print("STATING RECODING pos:" , recode_position, ", FROM ECC ", recode_from_ecc, ", to:", recode_to_ecc)    

            recoding_current_address =  (recode_position * dftm_iram_page_size) + recode_count
            print("RECODING " , recode_position, " - ", recode_count, " - ", recoding_current_address)
            
            if current_recoding_mode == RECODING_MODE.READ:
                print(current_recoding_mode, recoding_current_address)
                host_intf_sdram.addr_i.next = recoding_current_address
                host_intf_sdram.rd_i.next = 1
                current_recoding_mode.next = RECODING_MODE.WAIT_READ

            #if current_recoding_mode == RECODING_MODE.WAIT_READ:
            #    """Need wait 1 cycle to wait the READ really happen"""
            #    current_recoding_mode.next = RECODING_MODE.WAIT_READ_1

            if current_recoding_mode == RECODING_MODE.WAIT_READ:
                host_intf_sdram.rd_i.next = 0
                print(current_recoding_mode)
                if host_intf_sdram.done_o:
                    current_recoding_mode.next = RECODING_MODE.WRITE
                    recode_data_o.next = ecc.decoder(host_intf_sdram.data_o, recode_from_ecc)
                    """TODO IGNORING THE DECODE ERROR - Having not todo here ... """
                    print("RECODING READ ", host_intf_sdram.data_o)

            if current_recoding_mode == RECODING_MODE.WRITE:
                print(current_recoding_mode)
                host_intf_sdram.addr_i.next = recoding_current_address
                #recode_current_ecc
                host_intf_sdram.data_i.next = ecc.encoder(recode_data_o, recode_to_ecc)
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE

            if current_recoding_mode == RECODING_MODE.WAIT_WRITE:
                print(current_recoding_mode)
                host_intf_sdram.wr_i.next = 1

                if host_intf_sdram.done_o:
                    host_intf_sdram.rd_i.next = 0
                    host_intf_sdram.wr_i.next = 0
                    r_count =  recode_count +1
                    if r_count < dftm_iram_page_size:
                        current_recoding_mode.next = RECODING_MODE.WAIT_WRITE_1
                        recode_count.next = r_count
                    else:
                        """RECODING DONE"""
                        host_intf.done_o.next = True
                        current_operation_mode.next = OPERATION_MODE.NORMAL

                        ram_inf = ram[recode_position]
                        dftm_ram.set_encode(ram_inf, recode_to_ecc)
                        print("Change encode pos:", recode_position, ", from:" , recode_from_ecc, ",to:", recode_to_ecc )

            """Need wait 2 cycle to wait the WRITE really happen"""
            if current_recoding_mode == RECODING_MODE.WAIT_WRITE_1:                
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE_2
            if current_recoding_mode == RECODING_MODE.WAIT_WRITE_2:
                current_recoding_mode.next = RECODING_MODE.READ

                    

    return main