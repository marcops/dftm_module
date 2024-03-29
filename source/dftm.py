from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from ecc_64 import *
from ext_intf import *
from definitions import *
from enum import Enum

@block
def dftm(clk_i, ext_intf, sdram_mod1, sdram_mod2, dftm_iram_page_size = 2000,
    cycle_size = 1000000, error_decrease_by_cycle = 1 , error_increase = 1 , c_parity = 0,  c_hamming = 2, c_lpc = 4 ):

    iram_send = Signal(bool(0))
    OPERATION_MODE = enum('NORMAL','RECODING_UP', 'RECODING_DOWN')
    current_operation_mode = Signal(OPERATION_MODE.NORMAL)
    
    """INTERNAL RAM START"""
    #IRAM_DATA_SIZE = 1 + 2 + 5 + 32
    

    IRAM_ADDR_AMOUNT = 4 # * 1000 #96kb
    ram = [Signal(intbv(0)[IRAM_DATA_SIZE:0]) for i in range(IRAM_ADDR_AMOUNT)]
    """INTERNAL RAM END"""
    
    """RECODE """
    RECODING_MODE = enum('READ', 'WAIT_READ', 'WRITE', 'WAIT_WRITE', 'WAIT_WRITE_1', 'WAIT_WRITE_2')
    current_time = Signal(intbv(0)[128:])
    evaluate_recode = Signal(bool(False))
    recode_original_data = Signal(intbv(0)[WORD_SIZE:])
    ecc_counter = Signal(intbv(0)[WORD_SIZE:])
    ECC_DOUBLE_DATA = 7
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
        current_time.next = current_time + 1
        if current_time % cycle_size == 0:
            evaluate_recode.next = True

        if current_operation_mode == OPERATION_MODE.NORMAL:
            if ext_intf.dftm_i:
                if ext_intf.bf_i == 0:
                    if iram_send:
                        ext_intf.done_o.next = 1
                        iram_send.next = 0
                    else:                    
                        ext_intf.done_o.next = 0
                        iram_send.next = 1
                        #memory DFTM
                        if ext_intf.rd_i:
                            ext_intf.data_o.next = ram[ext_intf.addr_i]
                            if ext_intf.data_i < ECC_DOUBLE_DATA:
                                if ecc_counter > 0:
                                    ecc_counter.next = ecc_counter - 1
                                
                            #print("rd" , ram[ext_intf.addr_i])                    
                        if ext_intf.wr_i:
                            ram[ext_intf.addr_i].next = int(ext_intf.data_i)
                            if ext_intf.data_i >= ECC_DOUBLE_DATA:
                                ecc_counter.next = ecc_counter + 1
                               
                        
                        if ecc_counter == 0:
                            ext_intf.double_ecc.next = False
                        else:
                            ext_intf.double_ecc.next = True
                            #print("wd" , int(ext_intf.data_i))                    
                else:
                    sdram_mod1.rd_i.next = ext_intf.rd_i
                    sdram_mod1.wr_i.next = ext_intf.wr_i 
                    sdram_mod1.addr_i.next = ext_intf.addr_i
                    sdram_mod1.data_i.next = ext_intf.data_i_ecc
                    
                    ext_intf.done_o.next = sdram_mod1.done_o
                    ext_intf.data_o_ecc.next = sdram_mod1.data_o
            else:
                #memory SDRAM
                

                iram_current_position = dftm_ram.get_position(ext_intf.addr_i, dftm_iram_page_size)
                #print("RECODE 1.a ", ext_intf.addr_i)
                current_encode = 0
                #is_dynamic = 0
                ram_inf = ram[0]
                """Accessing a area major than managed, we will read without encode"""
                if iram_current_position < IRAM_ADDR_AMOUNT:                    
                    ram_inf = ram[iram_current_position]
                    
                    #print("RAM POS 1:", iram_current_position, ram_inf, ext_intf.addr_i, ext_intf.rd_i,ext_intf.wr_i, sdram_mod2.data_i)
                    #print("RAM POS 2:", ext_intf.data_o, ext_intf.done_o,ext_intf.rdPending_o)
                   # is_dynamic = dftm_ram.get_configuration(ram_inf)
                    #print("IS DYNAMIC" + str(is_dynamic))
                    current_encode = dftm_ram.get_encode(ram_inf)      
                    #print("rinfo", current_encode)          
                    #print("is_dynamic", is_dynamic)

                #print("CUR-ENCODE", host_intf.addr_i, "-",current_encode)
                sdram_mod1.addr_i.next = ext_intf.addr_i            
                sdram_mod1.rd_i.next = ext_intf.rd_i
                sdram_mod1.wr_i.next = ext_intf.wr_i
                ecc_val = ecc.encode(ext_intf.data_i, current_encode)
                sdram_mod1.data_i.next = ecc_val[WORD_SIZE_WITH_ECC:]
                
                if ecc.is_double_encode(current_encode):
                    sdram_mod2.addr_i.next = ext_intf.addr_i
                    sdram_mod2.rd_i.next = ext_intf.rd_i
                    sdram_mod2.wr_i.next = ext_intf.wr_i
                    sdram_mod2.data_i.next = ecc_val[WORD_DOUBLE_SIZE_WITH_ECC:WORD_SIZE_WITH_ECC]
                    #print(ecc_val[WORD_SIZE_WITH_ECC:])
                    #print(ecc_val[WORD_DOUBLE_SIZE_WITH_ECC:WORD_SIZE_WITH_ECC])
                #print(ecc_val)
                if sdram_mod1.rdPending_o == 1:
                    in_read.next = 1

                if sdram_mod1.done_o:
                    if in_read == 0:
                        ext_intf.done_o.next = sdram_mod1.done_o
                    else:  
                       
                        in_read.next = 0
                        n_data_o = intbv(0)[WORD_DOUBLE_SIZE_WITH_ECC:]
                        n_data_o |= sdram_mod1.data_o
                        #n_data_o = intbv(1)[WORD_DOUBLE_SIZE_WITH_ECC:]
                        if ecc.is_double_encode(current_encode):
                            n_data_o |= (sdram_mod2.data_o << WORD_SIZE_WITH_ECC)
                            
                        #print(n_data_o)
                        decode_ok = ecc.check(n_data_o, current_encode)

                        #have to recode init
                        
                      
                        if decode_ok == False:
                            n_err = int(dftm_ram.get_count_error(ram_inf))
                        #err Verilog here
                            n_err = n_err + error_increase
                            if n_err > 31:
                                n_err = 31                        
                            ram[iram_current_position].next = dftm_ram.set_count_error(ram[iram_current_position], n_err)
                        #    print("RECODE 1",  n_err,False, current_encode, current_encode, iram_current_position)
                        
                        #debug only
                        if  evaluate_recode == False:
                            #debug
                            n_err = int(dftm_ram.get_count_error(ram_inf))
                            #print("RECODE", now(),  n_err, current_encode, current_encode, iram_current_position)

                            ext_intf.recoded_o.next = False
                            ext_intf.data_o.next = ecc.decode(n_data_o, current_encode)
                            #print("OK_DECODING ", n_data_o, " - " , ext_intf.data_o)
                            ext_intf.done_o.next = sdram_mod1.done_o
                        else:
                            evaluate_recode.next = False
                            processed = False
                            for block_position in range(IRAM_ADDR_AMOUNT):
                                is_dynamic = dftm_ram.get_configuration(ram_inf)
                                n_err = int(dftm_ram.get_count_error(ram[block_position]))
                                current_encode = dftm_ram.get_encode(ram[block_position])
                                n_err = n_err - error_decrease_by_cycle
                                if n_err < 0:
                                    n_err = 0
                                ram[block_position].next = dftm_ram.set_count_error(ram[block_position], n_err)

                                next_encode = current_encode
                                if current_encode == 1  and n_err >= c_hamming:
                                    print("OOO hamming + ")
                                    next_encode = dftm_ram.get_next_encode(current_encode)                        
                                elif current_encode == 2  and n_err >= c_lpc:
                                    print("LPC + ")
                                    next_encode = dftm_ram.get_next_encode(current_encode)                        
                                elif current_encode == 3  and n_err < c_lpc:
                                    print("hamming bakc ")
                                    next_encode = dftm_ram.get_previous_encode(current_encode)    
                                elif current_encode == 2  and n_err < c_hamming:
                                    print("parity back ")
                                    next_encode = dftm_ram.get_previous_encode(current_encode)    
                                    
                                    
                                recode = (next_encode != current_encode and is_dynamic == 1)
                                print("RECODE", int(current_time), n_err, current_encode, next_encode, block_position)

                                if recode and processed == False: 
                                    n_err = int(dftm_ram.get_count_error(ram_inf))
                                    
                                    processed = True
                                    #position_change = block_position
                                    #print("recoding ", block_position)

                                    #if change_ecc:
                                        #position_change
                                    #print("OOO RECODE" , recode , is_up , next_encode , current_encode, current_encode, is_dynamic)
                                    current_operation_mode.next = OPERATION_MODE.RECODING_DOWN
                                    if next_encode > current_encode:
                                        current_operation_mode.next = OPERATION_MODE.RECODING_UP 

                                    current_recoding_mode.next = RECODING_MODE.READ
                                    recode_position.next = block_position                        
                                    recode_address.next = block_position * dftm_iram_page_size
                                    recode_from_ecc.next = current_encode
                                    recode_to_ecc.next = next_encode
                                    recode_count.next = 0
                                    ext_intf.done_o.next = False
                                    sdram_mod1.rd_i.next = False

                                    #3 = LPC
                                    if next_encode == 3 and current_encode == 2:
                                        ecc_counter.next = ecc_counter + 1
                                    elif next_encode == 2 and current_encode == 3:
                                        if ecc_counter > 0:
                                            ecc_counter.next = ecc_counter - 1

                                    if ecc_counter == 0:
                                        ext_intf.double_ecc.next = False
                                    else:
                                        ext_intf.double_ecc.next = True

                                    if ecc.is_double_encode(current_encode):
                                        sdram_mod2.rd_i.next = False
                            if processed == False:
                                n_err = int(dftm_ram.get_count_error(ram_inf))
                                

                                ext_intf.recoded_o.next = False
                                ext_intf.data_o.next = ecc.decode(n_data_o, current_encode)
                                #print("OK_DECODING ", n_data_o, " - " , ext_intf.data_o)
                                ext_intf.done_o.next = True

                        #if evaluate_recode: 
                            #print("RECODE 1",  n_err,False, current_encode, -2 , iram_current_position)
                        #else:
                        
                        
                              
                else:
                    ext_intf.done_o.next = sdram_mod1.done_o
                    #if in_read == 1:
                    #host_intf.data_o.next = ecc.decoder(sdram_mod1.done_o, current_encode)
                    #in_read.next = 0

                            
                        #sdram_mod1.wr_i.next = False
            #a = 0

               
 
        else:
            #RECODING MODE
            #if recode_count == 0 and current_recoding_mode == RECODING_MODE.READ:
            #print("STARTING RECODING pos:" , recode_position, ", FROM ECC ", recode_from_ecc, ", to:", recode_to_ecc)    
                    
            recoding_current_address =  (recode_position * dftm_iram_page_size) + recode_count
            #print("RECODING " , recode_position, " - ", recode_count, " - ", recoding_current_address)
            
            if current_recoding_mode == RECODING_MODE.READ:
                #print(current_recoding_mode, recoding_current_address)
                sdram_mod1.addr_i.next = recoding_current_address
                sdram_mod1.rd_i.next = 1
                if ecc.is_double_encode(recode_from_ecc):
                    sdram_mod2.addr_i.next = recoding_current_address
                    sdram_mod2.rd_i.next = 1

                current_recoding_mode.next = RECODING_MODE.WAIT_READ

            #if current_recoding_mode == RECODING_MODE.WAIT_READ:
            #    """Need wait 1 cycle to wait the READ really happen"""
            #    current_recoding_mode.next = RECODING_MODE.WAIT_READ_1

            if current_recoding_mode == RECODING_MODE.WAIT_READ:
                sdram_mod1.rd_i.next = 0
                if ecc.is_double_encode(recode_from_ecc):
                    sdram_mod2.rd_i.next = 0
                #print(current_recoding_mode)
                if sdram_mod1.done_o:
                    n_data_o = intbv(int(sdram_mod1.data_o))[WORD_DOUBLE_SIZE_WITH_ECC:]
                    #TODO AQUI
                    #n_data_o = intbv(1)[WORD_DOUBLE_SIZE_WITH_ECC:]
                    if ecc.is_double_encode(recode_from_ecc):
                        n_data_o |= ( sdram_mod2.data_o << WORD_SIZE_WITH_ECC)

                    current_recoding_mode.next = RECODING_MODE.WRITE
                    decoded_data = ecc.decode(n_data_o, recode_from_ecc)
                    ext_intf.recoded_o.next = True
                    recode_data_o.next = decoded_data

                    if recode_address == sdram_mod1.addr_i:
                        recode_original_data.next = decoded_data
                    """TODO IGNORING THE DECODE ERROR - Having not todo here ... """
                    #print("RECODING READ ", n_data_o)

            if current_recoding_mode == RECODING_MODE.WRITE:
                #print(current_recoding_mode)
                sdram_mod1.addr_i.next = recoding_current_address
                
                #recode_current_ecc
                ecc_val = ecc.encode(recode_data_o, recode_to_ecc)
                sdram_mod1.data_i.next = ecc_val[WORD_SIZE_WITH_ECC:]
                if ecc.is_double_encode(recode_to_ecc):
                    sdram_mod2.addr_i.next = recoding_current_address
                    sdram_mod2.data_i.next = ecc_val[WORD_DOUBLE_SIZE_WITH_ECC:WORD_SIZE_WITH_ECC]
                #print("RECODING WRITE ", ecc_val)
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE

            if current_recoding_mode == RECODING_MODE.WAIT_WRITE:
                #print(current_recoding_mode)
                sdram_mod1.wr_i.next = 1
                if ecc.is_double_encode(recode_to_ecc):
                    sdram_mod2.wr_i.next = 1

                if sdram_mod1.done_o:
                    sdram_mod1.rd_i.next = 0
                    sdram_mod1.wr_i.next = 0
                    if ecc.is_double_encode(recode_to_ecc):
                        sdram_mod2.rd_i.next = 0
                        sdram_mod2.wr_i.next = 0

                    r_count =  recode_count +1
                    if r_count < dftm_iram_page_size:
                        current_recoding_mode.next = RECODING_MODE.WAIT_WRITE_1
                        recode_count.next = r_count
                    else:
                        """RECODING DONE"""
                        #ext_intf.data_o.next = recode_original_data
                        #sdram_mod1.data_o.next = recode_original_data
                        ext_intf.done_o.next = True
                        current_operation_mode.next = OPERATION_MODE.NORMAL

                        ram_inf = ram[recode_position]
                        ram[recode_position].next = dftm_ram.set_encode(int(ram_inf), recode_to_ecc)

                        #Update all?
                        #for.. etc
                        #cur_cycle = now()//cycle_size
                        #dftm_ram.set_cycle(ram_inf,cur_cycle)
                        #print("Change encode pos:", recode_position, ", from:" , recode_from_ecc, ",to:", recode_to_ecc )

            """Need wait 2 cycle to wait the WRITE really happen"""
            if current_recoding_mode == RECODING_MODE.WAIT_WRITE_1:                
                current_recoding_mode.next = RECODING_MODE.WAIT_WRITE_2
            if current_recoding_mode == RECODING_MODE.WAIT_WRITE_2:
                current_recoding_mode.next = RECODING_MODE.READ

                    

    return main