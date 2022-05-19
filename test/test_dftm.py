from utils import *

def test_readwrite(host_intf):
    @instance
    def test():
        yield delay(140)  
        for i in range(5):
            yield write_dftm_ram(host_intf, i, 1)

        yield write_ram(host_intf, 120, 23)      
        
        yield read_ram(host_intf, 120)   
        t_asset_hex("Message Write with problem", host_intf.data_o, 23)

        #print("READING AGAIN")
        #yield write_ram(host_intf, 120, 23)      
        #yield read_ram(host_intf, 120)     

        
        
           
        
        yield read_dftm_ram(host_intf, 0)
        t_asset_hex("Encode with problem", host_intf.data_o , 3)
    return test

test_run_bench(signal = True, func = test_readwrite, timesteps=25000)
