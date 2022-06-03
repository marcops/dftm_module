from utils import *
import random

PROBABILITY = 0.1
SEED_NUMBER = 10
MAX_ADDRESS = 65534
MAX_DATA = 65534
def test_dftm_probability(host_intf, output):

    def configure_dftm():
        for i in range(5):
            yield write_dftm_ram(host_intf, i, (3<<1))
    
    def get_random_address():
        return random.randint(0, MAX_ADDRESS)
    def get_random_data():
        return random.randint(0, MAX_DATA)

    @instance
    def test():
        TOTAL_OF_CYCLES = 0

        random.seed(SEED_NUMBER)
        yield delay(140)        
        yield configure_dftm()

        while True:   
            TOTAL_OF_CYCLES += 1
            address = get_random_address()
            data = get_random_data()
            yield write_ram(host_intf, address, data)
            yield read_ram(host_intf, address)
            #t_asset_hex("test_dftm_probability " + ERR_MEM_DEFAULT, host_intf.data_o, data)


            #yield bit_flip(host_intf, address, [8])
   
            #yield read_ram(host_intf, address)
            #t_asset_hex("test_dftm_probability " + ERR_MEM_DEFAULT, host_intf.data_o, DATA_TO_WRITE)
            output['TOTAL_OF_CYCLES'] = TOTAL_OF_CYCLES
    
    return test



try:
    result = {}
    print("-------------------------------")
    print("STARTING WITH PROBABILITY: " + str(PROBABILITY) + "%")
    print("-------------------------------")
    test_run_bench(func=test_dftm_probability, timesteps=35000, output=result)

    print("-------------------------------")
    print("PROBABILITY: " + str(PROBABILITY) + "%")
    print("TOTAL_OF_CYCLES: " + str(result['TOTAL_OF_CYCLES']))
    print("-------------------------------")
except Exception as e:
    print("FAIL - test_dftm_probability - " + str(e))   
    raise e