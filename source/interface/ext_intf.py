from myhdl import *


class ExtIntf(object):

    def __init__(self):
        # Host side signals
        self.rst_i = ResetSignal(0, active=1, isasync=True)
        self.rd_i = Signal(bool(0))
        self.wr_i = Signal(bool(0))
        self.addr_i = Signal(intbv(0)[24:])  # host side address = sdram side row + col + bank
        #separar para ter 16
        self.data_i = Signal(intbv(0)[16:])
        self.data_o = Signal(intbv(0)[16:])
        self.done_o = Signal(bool(0))
        self.rdPending_o = Signal(bool(0))
        #add iram_dftm
        self.dftm_i = Signal(bool(0))

    def read(self, addr):
        self.dftm_i.next = 0
        self.addr_i.next = addr
        self.rd_i.next = 1
        yield delay(2)
        self.rd_i.next = 0

    def write(self, addr, data):
        self.dftm_i.next = 0
        self.addr_i.next = addr
        self.data_i.next = data
        yield delay(5)
        self.wr_i.next = 1

    def read_dftm(self, addr):
        self.dftm_i.next = 1
        self.addr_i.next = addr
        self.rd_i.next = 1
        #yield delay(2)
        #self.rd_i.next = 0

    def write_dftm(self, addr, data):
        self.dftm_i.next = 1
        self.addr_i.next = addr
        self.data_i.next = data
        self.wr_i.next = 1
        yield delay(3)
        self.wr_i.next = 0

    def nop(self):
        self.rd_i.next = 0
        self.wr_i.next = 0
        self.dftm_i.next = 0

    def wait_until_done(self):
        yield self.done_o.posedge

    #def read_data(self):
        #return self.data_o.val
