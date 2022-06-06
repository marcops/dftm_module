from utils import *
import random

#prob in percent
RANGE_PROBABILITY = 1
SEED_NUMBER = 10
MAX_ADDRESS = 32000
MAX_DATA = 65534
def test_dftm_probability(host_intf, output):
    
    def occur_bf():
        v = random.randint(0, 99)
        return v < RANGE_PROBABILITY

    def configure_dftm():
        total_of_pages = 128
        for i in range(total_of_pages):
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
            bf = occur_bf()
            if bf:
                print("WILL HAVE BF")
                yield bit_flip(host_intf, address, [8])

            yield read_ram(host_intf, address)            
            t_asset_hex("test_dftm_probability " + ERR_MEM_DEFAULT, host_intf.data_o, data)
            
            output['TOTAL_OF_CYCLES'] = TOTAL_OF_CYCLES
            if bf:
                yield delay(350)
            else:
                yield delay(100)
    return test



try:
    result = {}
    print("-------------------------------")
    print("STARTING WITH PROBABILITY: " + str(RANGE_PROBABILITY) + "%")
    print("-------------------------------")
    test_run_bench(func=test_dftm_probability, timesteps=1450000, output=result)

    print("-------------------------------")
    print("PROBABILITY: " + str(RANGE_PROBABILITY) + "%")
    print("TOTAL_OF_CYCLES: " + str(result['TOTAL_OF_CYCLES']))
    print("-------------------------------")
except Exception as e:
    print("FAIL - test_dftm_probability - " + str(e))   
    raise e