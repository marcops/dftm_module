from myhdl import *

from dftm import dftm

def convert_inc(hdl):
    """Convert inc block to VHDL."""

    ecc_type = Signal(intbv(0)[2:])
    address = Signal(intbv(0)[16:])
    command = intbv(0)

    dftm_1 = dftm(ecc_type, address, command)

    dftm_1.convert(hdl=hdl)

convert_inc(hdl='VHDL')