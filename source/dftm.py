from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from ecc import *
from ext_intf import *
from definitions import *
from enum import Enum

@block
def dftm(clk_i, ext_intf, sdram_mod1, sdram_mod2, dftm_iram_page_size = 256):
    iram_send = Signal(bool(0))
    OPERATION_MODE = enum('NORMAL','RECODING_UP', 'RECODING_DOWN')
    current_operation_mode = Signal(OPERATION_MODE.NORMAL)
    
    """INTERNAL RAM START"""
    IRAM_DATA_SIZE = 3
    IRAM_ADDR_AMOUNT = 256 # * 1000 #96kb
    ram = [Signal(intbv(0)[IRAM_DATA_SIZE:0]) for i in range(IRAM_ADDR_AMOUNT)]
    """INTERNAL RAM END"""
    
    """RECODE """
    RECODING_MODE = enum('READ', 'WAIT_READ', 'WRITE', 'WAIT_WRITE', 'WAIT_WRITE_1', 'WAIT_WRITE_2')
    
    recode_original_data = Signal(intbv(0)[WORD_SIZE:])
    recode_address = Signal(intbv(0)[24:]) 
    recode_position = Signal(intbv(0)[24:]) 
    recode_count = Signal(intbv(0)[24:]) 
    recode_data_o = Signal(intbv(0)[WORD_SIZE:])
    recode_from_ecc = Signal(intbv(0)[IRAM_DATA_SIZE:])
    recode_to_ecc = Signal(intbv(0)[IRAM_DATA_SIZE:])
    current_recoding_mode = Signal(RECODING_MODE.READ)
    in_read = Signal(bool(0))
    """END RECODE"""

    @always(clk_i.posedge)
    def main():        
        if current_operation_mode == OPERATION_MODE.NORMAL:
            if ext_intf.dftm_i:
                if iram_send:
                    ext_intf.done_o.next = 1
                    iram_send.next = 0
                else:
                    #memory DFTM
                    if ext_intf.rd_i:
                        ext_intf.data_o.next = ram[ext_intf.addr_i]
                        ext_intf.done_o.next = 0
                        iram_send.next = 1
                    if ext_intf.wr_i:
                        ram[ext_intf.addr_i].next = int(ext_intf.data_i)
                        print("WR", ext_intf.addr_i, "-", ext_intf.data_i)
                        ext_intf.done_o.next = 0
                        iram_send.next = 1
            else:
                #memory SDRAM
                iram_current_position = dftm_ram.get_position(ext_intf.addr_i, dftm_iram_page_size)
                current_encode = 0
                is_dynamic = 0
                """Accessing a area major than managed, we will read without encode"""
                if iram_current_position < IRAM_ADDR_AMOUNT:                    
                    ram_inf = ram[iram_current_position]
                    #print("RAM POS", iram_current_position, "-",ram_inf)
                    is_dynamic = dftm_ram.get_configuration(ram_inf)
                    is_dynamic = 1
                    current_encode = dftm_ram.get_encode(ram_inf)
                #print("CUR-ENCODE", host_intf.addr_i, "-",current_encode)
                sdram_mod1.addr_i.next = ext_intf.addr_i            
                sdram_mod1.rd_i.next = ext_intf.rd_i
                sdram_mod1.wr_i.next = ext_intf.wr_i
                sdram_mod1.data_i.next = ext_intf.data_i
                #print_sig("r",sdram_mod1)
                if sdram_mod1.rdPending_o == 1:
                    in_read.next = 1

                if sdram_mod1.done_o:
                    if in_read == 0:
                        ext_intf.done_o.next = sdram_mod1.done_o
                    else:  
                        in_read.next = 0                    
                        decode_ok = ecc.check(sdram_mod1.data_o, current_encode)
                        
                        #TODO DEBUG BITFLIP AT ADDRESS 120 
                        if ext_intf.addr_i == 120:
                            decode_ok = 0

                        if decode_ok:
                            ext_intf.data_o.next = ecc.decode(sdram_mod1.data_o, current_encode)
                            ext_intf.done_o.next = sdram_mod1.done_o
                        else:                        
                            next_encode = dftm_ram.get_next_encode(current_encode)                        
                            recode = (next_encode != current_encode and is_dynamic == 1)
                            print("will recode:", recode)
                            print("Code?:", next_encode != current_encode)
                            print("Dyn?:", is_dynamic)
                            if recode:
                                current_operation_mode.next = OPERATION_MODE.RECODING_UP
                                current_recoding_mode.next = RECODING_MODE.READ
                                recode_position.next = iram_current_position
                                recode_address.next = ext_intf.addr_i
                                recode_from_ecc.next = current_encode
                                recode_to_ecc.next = next_encode
                                recode_count.next = 0
                                ext_intf.done_o.next = False
                                sdram_mod1.rd_i.next = False
                                #sdram_mod1.wr_i.next = False
                            else:
                                ext_intf.data_o.next = ecc.decode(sdram_mod1.data_o, current_encode)
                                ext_intf.done_o.next = sdram_mod1.done_o
                                in_read.next = 0
                else:
                    ext_intf.done_o.next = sdram_mod1.done_o
                    #if in_read == 1:
                    #host_intf.data_o.next = ecc.decoder(sdram_mod1.done_o, current_encode)
                    #in_read.next = 0
 
        else:
            #RECODING MODE
            if recode_count == 0 and current_recoding_mode == RECODING_MODE.READ:
                print("STARTING RECODING pos:" , recode_position, ", FROM ECC ", recode_from_ecc, ", to:", recode_to_ecc)    
                    
            recoding_current_address =  (recode_position * dftm_iram_page_size) + recode_count
            print("RECODING " , recode_position, " - ", recode_count, " - ", recoding_current_address)
            
            if current_recoding_mode == RECODING_MODE.READ:
                print(current_recoding_mode, recoding_current_address)
                sdram_mod1.addr_i.next = recoding_current_address
                sdram_mod1.rd_i.next = 1
                current_recoding_mode.next = RECODING_MODE.WAIT_READ

            #if current_recoding_mode == RECODING_MODE.WAIT_READ:
            #    """Need wait 1 cycle to wait the READ really happen"""
            #    current_recoding_mode.next = RECODING_MODE.WAIT_READ_1

            if current_recoding_mode == RECODING_MODE.WAIT_READ:
                sdram_mod1.rd_i.next = 0
                print(current_recoding_mode)
                if sdram_mod1.done_o:
                    current_recoding_mode.next = RECODING_MODE.WRITE
                    decoded_data = ecc.decode(sdram_mod1.data_o, recode_from_ecc)
                    recode_data_o.next = decoded_data
                    #debug propose
                    recode_data_o.next = ecc.decode(sdram_mod1.data_o, recode_from_ecc) + 1
                    if recode_address == sdram_mod1.addr_i:
                        recode_original_data.next = decoded_data
                    """TODO IGNORING THE DECODE ERROR - Having not todo here ... """
                    print("RECODING READ ", sdram_mod1.data_o)

            if current_recoding_mode == RECODING_MODE.WRITE:
                print(current_recoding_mode)
                sdram_mod1.addr_i.next = recoding_current_address
                #recode_current_ecc
                sdram_mod1.data_i.next = ecc.encode(recode_data_o, recode_to_ecc)
                print("RECODING WRITE ", sdram_mod1.data_o)
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE

            if current_recoding_mode == RECODING_MODE.WAIT_WRITE:
                print(current_recoding_mode)
                sdram_mod1.wr_i.next = 1

                if sdram_mod1.done_o:
                    sdram_mod1.rd_i.next = 0
                    sdram_mod1.wr_i.next = 0
                    r_count =  recode_count +1
                    if r_count < dftm_iram_page_size:
                        current_recoding_mode.next = RECODING_MODE.WAIT_WRITE_1
                        recode_count.next = r_count
                    else:
                        """RECODING DONE"""
                        ext_intf.data_o.next = recode_original_data
                        sdram_mod1.data_o.next = recode_original_data
                        ext_intf.done_o.next = True
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