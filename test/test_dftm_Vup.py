from utils import *
import random

#prob in percent
#100% = 10000
# 10% = 1000
#  1% = 100
#0.1% = 10
#0.01% = 1
RANGE_PROBABILITY = 1 * 100 
SEED_NUMBER = 10
MAX_ADDRESS = 32000
MAX_DATA = 65534
def test_dftm_probability(host_intf, output):
    
    def occur_bf():
        v = random.randint(0, 9999)
        return v < RANGE_PROBABILITY
    def configure_dftm():
        total_of_pages = 128
        for i in range(total_of_pages):
            yield write_dftm_ram(host_intf, i, 5)    
    def random_address():
        return random.randint(0, MAX_ADDRESS)
    def random_data():
        return random.randint(0, MAX_DATA)
    def get_list_bf():
        lst = []
        amount = random_amount_bf()
        for i in range(amount):
            lst.append(random_position_bf())
        return list( dict.fromkeys(lst) )
    def random_amount_bf():
        return random.randint(1, 3)
    def random_position_bf():
        return random.randint(0, WORD_SIZE-1)
    def lst_2_str(lst):
        s = ""
        for i in lst:
            s += str(i)+"-"
        return s

    @instance
    def test():
        TOTAL_OF_CYCLES = 0

        random.seed(SEED_NUMBER)
        yield delay(140)        
        yield configure_dftm()

        while True:   
            TOTAL_OF_CYCLES += 1
            address = random_address()
            data = random_data()
            yield write_ram(host_intf, address, data)
            bf = occur_bf()
            if bf:
                lst = get_list_bf()
                print("RECODE 0", now(), address, lst_2_str(lst), len(lst))
                yield bit_flip(host_intf, address, lst)

            yield read_ram(host_intf, address)            
            #t_asset_hex("test_dftm_probability " + ERR_MEM_DEFAULT, host_intf.data_o, data)
            if bf:
                print("RECODE 2", data ,host_intf.data_o , data == host_intf.data_o)
            
            output['TOTAL_OF_CYCLES'] = TOTAL_OF_CYCLES
     
    return test

try:
    result = {}
    print("-------------------------------")
    print("STARTING WITH PROBABILITY: " + str(RANGE_PROBABILITY) + "%")
    print("-------------------------------")
    test_run_bench(func=test_dftm_probability, timesteps=1450000, output=result, ctrl_type=1)

    print("-------------------------------")
    print("PROBABILITY: " + str(RANGE_PROBABILITY) + "%")
    print("TOTAL_OF_CYCLES: " + str(result['TOTAL_OF_CYCLES']))
    print("-------------------------------")
except Exception as e:
    print("FAIL - test_dftm_probability - " + str(e))   
    raise e