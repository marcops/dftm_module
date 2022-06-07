import sys
import random
from myhdl import Signal, delay, instance
sys.path.insert(0, 'source')
sys.path.insert(1, 'source/interface')

from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from sdram_cntl_direct import *
from dftm import *

ERR_MEM_DEFAULT = "READ/WRITE with problem"
ERR_DFTM_MEM_DEFAULT = "DFTM MEM with problem"

def get_random_address():
    return random.randint(0, 32000)
def get_random_data():
    return random.randint(0, 65534)

def bit_flip(host_intf, address, lst_pos):
    for pos in lst_pos:
        yield read_bf(host_intf, address)
        #print("READ " , str(host_intf.data_o_ecc))
        if (host_intf.data_o >>pos) & 1 == 1:
            n_data = (int(host_intf.data_o_ecc) ^ (0 << pos))
        else:
            n_data = (int(host_intf.data_o_ecc) ^ (1 << pos))
        #print("N DATA " , str(n_data))
        yield write_bf(host_intf, address, n_data)
        yield delay(10)

def t_asset_hex(msg, data, data_expect):
    data = hex(data)
    data_expect = hex(data_expect)
    if data != data_expect:
        print("[TEST FAIL] "+ msg + " rec:" + str(data) + ", expect:" + str(data_expect))
        raise Exception("TEST FAIL")

def read_bf(host_intf, addr):
    yield host_intf.read_bf(addr)
    yield host_intf.done_o.posedge
    yield delay(3)
    print("[BF-READ] addr: " , hex(addr) , ", data: ", hex(host_intf.data_o))

def write_bf(host_intf, addr, data):
    yield host_intf.write_bf(addr, data)
    yield host_intf.done_o.posedge
    yield host_intf.nop()
    yield delay(3)
    print("[BF-WRITE] addr: " , hex(addr) , ", data: ", hex(data))

def write_dftm_ram(host_intf, addr,data):
    yield host_intf.write_dftm(addr, data)
    yield host_intf.done_o.posedge
    yield host_intf.nop()    
    print("[CPU-DFTM-WRITE] addr: " , hex(addr) , ", data: ", hex(data))

def write_ram(host_intf, addr,data):
    yield host_intf.write(addr, data)
    yield host_intf.done_o.posedge
    yield host_intf.nop()
    yield delay(5)
    print("[CPU-WRITE] addr: " , hex(addr) , ", data: ", hex(data))

def read_dftm_ram(host_intf, addr):
    yield host_intf.read_dftm(addr)
    yield host_intf.done_o.posedge
    yield host_intf.nop()
    #yield delay(1)
    print("[CPU-READ] addr: " , hex(addr) , ", data: ", hex(host_intf.data_o))

def read_ram(host_intf, addr):
    yield host_intf.read(addr)
    yield host_intf.done_o.posedge
    yield delay(3)
    print("[CPU-READ] addr: " , hex(addr) , ", data: ", hex(host_intf.data_o))


def test_run_bench(signal = False, func = None, timesteps = 5000, output = None, ctrl_type = 0):
    if func is None:
        print("TEST FAIL - need a function")
        return;
        
    clk_i = Signal(bool(0))
    #rst_i = ResetSignal(0, active=1, isasync=True)

    clkDriver_Inst = clk_driver(clk_i)
    sd_intf_Inst1 = SdramIntf()
    sd_intf_Inst2 = SdramIntf()
    ext_intf_Inst = ExtIntf()
    host_intf_sdram_Inst1 = HostIntf()
    host_intf_sdram_Inst2 = HostIntf()

    sdram_Inst1 = sdram(clk_i, sd_intf_Inst1, show_command=False)
    sdram_Inst2 = sdram(clk_i, sd_intf_Inst2, show_command=False)
    if ctrl_type == 0:
        sdramCntl_Inst1 = sdram_cntl(clk_i, host_intf_sdram_Inst1, sd_intf_Inst1)
        sdramCntl_Inst2 = sdram_cntl(clk_i, host_intf_sdram_Inst2, sd_intf_Inst2)
    if ctrl_type == 1:
        sdramCntl_Inst1 = sdram_cntl_direct(clk_i, host_intf_sdram_Inst1, sd_intf_Inst1)
        sdramCntl_Inst2 = sdram_cntl_direct(clk_i, host_intf_sdram_Inst2, sd_intf_Inst2)

    dftm_Inst = dftm(clk_i, ext_intf_Inst, host_intf_sdram_Inst1, host_intf_sdram_Inst2)
    if output is not None:
        test_readWrite_Inst = func(ext_intf_Inst, output)
    else:
        test_readWrite_Inst = func(ext_intf_Inst)
    if signal:
        dftm_Inst = traceSignals(dftm_Inst,sdramCntl_Inst1,sdramCntl_Inst2, ext_intf_Inst, sd_intf_Inst1, sd_intf_Inst2)

    sim = Simulation(clkDriver_Inst, sdram_Inst1, sdram_Inst2, sdramCntl_Inst1,sdramCntl_Inst2, dftm_Inst, test_readWrite_Inst)
    sim.run(timesteps)