from math import ceil
#from turtle import position

from numpy import True_
from sd_intf import *
from host_intf import *
from dftm import *

@block
def sdram_cntl_direct(clk_i, host_intf, sd_intf):
    
    state = enum('NOP', 'WRITE', 'READ', 'LOAD','ACTIVATE')
    initialized = Signal(bool(0))
    processing = Signal(bool(0))
    next_nop = Signal(intbv(0)[4:])      
    driver = sd_intf.get_driver()

    @always(clk_i.posedge)
    def main():
        sd_intf.cke.next = 1

        if processing == 0:
            if host_intf.rd_i == 1:
                processing.next = 1
                sd_intf.bs.next = int(host_intf.addr_i/8192)
                sd_intf.addr.next = host_intf.addr_i%8192
                # [READ] # cs ras cas we dqm : L H L H X
                self.cs.next, self.ras.next, self.cas.next, self.we.next = 0, 1, 0, 1
                yield clk.posedge
                yield clk.posedge

            if host_intf.wr_i == 1:
                processing.next = 1

        else:
            processing.next = 0
        
        # sd_intf.nop(clk)
        # yield delay(5000)
        # yield sd_intf.load_mode(clk)

        # for p in range(4):            
        #     yield sd_intf.nop(clk)
        #     yield sd_intf.activate(clk, 17, bank_id=p)
        #     yield sd_intf.nop(clk)
        #     yield delay(10000)
        # #yield delay(10000)
        # while True:
        #     address = get_random_address()
        #     data = get_random_data()

        #     print(address)
        #     bank_id = int(address/8192)
        #     address = address%8192
        #     #print(address)            
        #     #print(bank_id)
        #     yield sd_intf.nop(clk)
        #     yield sd_intf.write(clk, driver, address, data,bank_id=bank_id)
        #     yield sd_intf.nop(clk)
        #     yield delay(10)
        #     yield sd_intf.read(clk, address, bank_id)
        #     yield sd_intf.nop(clk)
        #     yield delay(4)
        #     t_asset_hex("test_readwrite ", sd_intf.dq, data)
        
    return main

    
    

    

