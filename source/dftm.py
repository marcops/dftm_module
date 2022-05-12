from myhdl import *
from dftm_ram import *
from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *


@block
def dftm(clk_i, host_intf, host_intf_sdram):
    #PAGE_SIZE - should be dynamic in the future
    PAGE_SIZE = 256
    dftm_mem_addr = host_intf.addr_i // PAGE_SIZE 

    CONFIGURATION_TYPE = {
        'STATIC': 0,
        'AUTOMATIC': 1
    }

    ENCODE_TYPE = {
        'NONE':0,
        'PARITY':1,
        'HAMMING':2,
        'REED_SOLOMON':3
    }   


    """DFTM internal memory signals"""
    MEM_ADDR_WIDTH = 3
    MEM_WIDTH = 256
    mem_data_in = Signal(intbv(0)[MEM_ADDR_WIDTH:0])
    mem_data_out = Signal(intbv(0)[MEM_ADDR_WIDTH:0])
    i_ram = dftm_ram(clk_i, host_intf.wr_i, dftm_mem_addr, mem_data_in, mem_data_out, MEM_ADDR_WIDTH, MEM_WIDTH)
    """END DFTM internal memory signals"""
   
    def get_encode():
        return mem_data_out>>1
    def get_configuration():
        return mem_data_out & 0x1

    def set_configuration(config):
        mem_data_in.next[0] = config        
    def set_encode(enc):
        mem_data_in.next[1] = (enc & 0x1)
        mem_data_in.next[2] = (enc & 0x2) >> 1

    #@always_comb
    #def pin_ports3():
        #host_intf.rdPending_o.next =  host_intf_sdram.rdPending_o

    @always(host_intf.wr_i)
    def on_write():
        #host_intf_sdram.done_o.next = host_intf.done_o
        host_intf_sdram.addr_i.next = host_intf.addr_i
        host_intf_sdram.data_i.next = host_intf.data_i
        host_intf_sdram.wr_i.next = host_intf.wr_i

    @always(host_intf_sdram.done_o)
    def when_done():
        host_intf.wr_i.next = host_intf_sdram.wr_i  
        host_intf.rd_i.next = host_intf_sdram.rd_i

        host_intf.done_o.next = host_intf_sdram.done_o
        host_intf.data_o.next = host_intf_sdram.data_o

    @always(host_intf.rd_i)
    def on_read():
        host_intf_sdram.done_o.next = host_intf.done_o
        host_intf_sdram.addr_i.next = host_intf.addr_i
        host_intf_sdram.rd_i.next = host_intf.rd_i
     

    #@always(host_intf.rd_i)
    #def on_read():
        #"""Controller DFTM  - on read data """   
        #encode = get_encode()
        #print(encode)        
        #configuration = get_configuration()
        #print(configuration)

    #@always(host_intf.wr_i)
    #def on_write():
        #"""Controller DFTM  - on write data """   
        #ecc.next = get_encode()        
        #print(ecc)

    def fake_ecc_encode():
        print("FAKE ECC ENCODE...")

    def fake_ecc_decode():
        print("FAKE ECC DECODE...")

    return on_write, on_read, when_done, i_ram