from math import ceil
#from turtle import position

from numpy import True_
from sd_intf import *
from host_intf import *
from dftm import *

@block
def sdram_cntl_direct(clk_i, host_intf, sd_intf):
    
    iram_send = Signal(bool(0))
    address_read = Signal(intbv(0)[24:0])
    ram = [Signal(intbv(0)[WORD_SIZE_WITH_ECC:0]) for i in range(32000)]

    @always(clk_i.posedge)
    def seq_func():
        #print(iram_send, host_intf.rd_i, host_intf.wr_i ,  host_intf.addr_i, address_read,  ram[address_read] )
        #host_intf.data_o.next = ram[address_read]                        
        
        if iram_send:
            host_intf.done_o.next = 1
            iram_send.next = 0
            host_intf.rdPending_o.next = 0
        else:   
            host_intf.done_o.next = 0
            if host_intf.rd_i:                
                iram_send.next = 1    
                host_intf.rdPending_o.next = 1
                address_read.next = host_intf.addr_i
                host_intf.data_o.next = ram[ host_intf.addr_i]   
                #print("rd" , host_intf.addr_i, ram[host_intf.addr_i])
            elif host_intf.wr_i:
                iram_send.next = 1
                val = int(host_intf.data_i)
                ram[host_intf.addr_i].next = val
                #print("wd" , host_intf.addr_i, val)
        
    return seq_func

    
    

    

