from myhdl import *
from dftm_ram import *

@block
def dftm(clk_i, host_intf, cmd_x, sd_intf):
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
        

    @always(host_intf.rd_i)
    def on_read():
        encode = get_encode()        
        print(encode)        
        configuration = get_configuration()
        print(configuration)
        
        #print(dftm_mem_addr)
        #position
        #pos = discover_current_ecc()
        #print("Reading encode "+str(dout) )
        #position = host_intf.addr_i // PAGE_SIZE
       # val = memory_1[position] + (memory_2[position] << 1)
        #print("read" + str(value))
        #print("DFTM-READ [add=" + str(host_intf.addr_i) + ", pos="+str(position) + "]")

    @always(host_intf.wr_i)
    def on_write():
        #print("change Encode "+str(din))
        mem_data_in.next[1] = 1
        mem_data_in.next[0] = 0
        #memory_1[0] = True
        #print("write" + str(value))
    #    position = discover_current_ecc(host_intf.addr_i)
    #    print("DFTM-WRITE [add=" + str(host_intf.addr_i) + ", pos="+str(position) + "]")

    return on_read, on_write, i_ram