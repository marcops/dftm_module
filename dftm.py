from myhdl import *

@block
def dftm(clk_i, host_intf, cmd_x, sd_intf):
    #PAGE_SIZE - shoud be dynamic 
    PAGE_SIZE = 256
    MEMORY_SIZE = 256
    
    memory_1 = Signal(intbv(0)[MEMORY_SIZE:0])
    memory_2 = Signal(intbv(0)[MEMORY_SIZE:0])
   
    def discover_current_ecc(address):
        position = address // PAGE_SIZE
        return memory_1[position] + (memory_2[position] << 1)

    @always(host_intf.rd_i)
    def on_read():
        x = discover_current_ecc(host_intf.addr_i)
        #print("reading - " + str(host_intf.addr_i))

    @always(host_intf.wr_i)
    def on_write():
        x = discover_current_ecc(host_intf.addr_i)
        #print("writing - " + str(host_intf.addr_i))

    return on_read, on_write