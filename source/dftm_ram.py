from myhdl import *

@block
def dftm_ram(clk, we, addr, din, dout, addr_width=2, data_width=3) :
    ram_single_port = [Signal(intbv(0)[addr_width:0]) for i in range(data_width)]

    @always(clk.posedge)
    def write_logic():
        """Controller DFTM Memory - write data to address 'addr' """
        if we == 1:           
            ram_single_port[addr].next = din

    @always_comb
    def read_logic():
        """Controller DFTM Memory - read data from address 'addr' """        
        dout.next = ram_single_port[addr]
    return read_logic, write_logic
