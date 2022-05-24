import sys

from myhdl import Signal, delay, instance
sys.path.insert(0, 'source')

from clk_driver import clk_driver
from sdram import *
from sdram_cntl import *
from dftm import *

ERR_MEM_DEFAULT = "READ/WRITE with problem"
ERR_DFTM_MEM_DEFAULT = "DFTM MEM with problem"

def t_asset_hex(msg, data, data_expect):
    data = hex(data)
    data_expect = hex(data_expect)
    if data != data_expect:
        print("[TEST FAIL] "+ msg + " rec:" + str(data) + ", expect:" + str(data_expect))
        raise Exception("TEST FAIL")

def write_dftm_ram(host_intf, addr,data):
    yield host_intf.write_dftm(addr, data)
    yield host_intf.done_o.posedge
    yield host_intf.nop()    
    print("[CPU-DFTM-WRITE] addr: " , hex(addr) , ", data: ", hex(data))

def write_ram(host_intf, addr,data):
    yield host_intf.write(addr, data)
    yield host_intf.done_o.posedge
    yield host_intf.nop()
    yield delay(3)
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


def test_run_bench(signal = False, func = None, timesteps = 5000):
    if func is None:
        print("TEST FAIL - need a function")
        return;
        
    clk_i = Signal(bool(0))
    #rst_i = ResetSignal(0, active=1, isasync=True)

    clkDriver_Inst = clk_driver(clk_i)
    sd_intf_Inst = SdramIntf()
    ext_intf_Inst = ExtIntf()
    host_intf_sdram_Inst = HostIntf()

    sdram_Inst = sdram(clk_i, sd_intf_Inst, show_command=False)
    sdramCntl_Inst = sdram_cntl(clk_i, host_intf_sdram_Inst, sd_intf_Inst)
    dftm_Inst = dftm(clk_i, ext_intf_Inst, host_intf_sdram_Inst)
    test_readWrite_Inst = func(ext_intf_Inst)
    if signal:
        dftm_Inst = traceSignals(dftm_Inst,sdramCntl_Inst, ext_intf_Inst, sd_intf_Inst)

    sim = Simulation(clkDriver_Inst, sdram_Inst, sdramCntl_Inst, dftm_Inst, test_readWrite_Inst)
    sim.run(timesteps)